"""Light Monitor - Orchestrates light detection and recommendations"""
import logging
import asyncio
from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
from threading import Thread, Event

from .camera_manager import AmbientLightDetector
from .screen_brightness import ScreenBrightness


class LightMonitor:
    """Monitors ambient light and provides recommendations"""
    
    def __init__(self, 
                 config: Dict,
                 ai_client = None,
                 callback: Optional[Callable] = None):
        """
        Initialize light monitor
        
        Args:
            config: Configuration dictionary
            ai_client: AI client for recommendations
            callback: Callback function for light updates
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.ai_client = ai_client
        self.callback = callback
        
        # Initialize components
        camera_index = config.get('camera_index', 0)
        self.light_detector = AmbientLightDetector(camera_index)
        self.brightness_control = ScreenBrightness()
        
        # Settings
        self.check_interval = config.get('check_interval_seconds', 30)
        self.auto_adjust_brightness = config.get('auto_adjust_brightness', False)
        
        # State
        self.running = False
        self.thread: Optional[Thread] = None
        self.stop_event = Event()
        
        self.current_lux = 0
        self.current_status = 'unknown'
        self.last_recommendation = None
        self.last_warning_time = None
        
        # Statistics
        self.light_history = []
        self.max_history_size = 100
    
    def start(self) -> bool:
        """Start light monitoring"""
        
        if self.running:
            self.logger.warning("Light monitor already running")
            return False
        
        # Try to initialize camera
        camera_init = self.light_detector.initialize()
        if camera_init:
            self.logger.info("Light monitoring started with webcam")
        else:
            self.logger.info("Light monitoring started with fallback method")
        
        self.running = True
        self.stop_event.clear()
        
        # Start monitoring thread
        self.thread = Thread(target=self._monitoring_loop, daemon=True)
        self.thread.start()
        
        return True
    
    def stop(self):
        """Stop light monitoring"""
        if not self.running:
            return
        
        self.logger.info("Stopping light monitor...")
        self.running = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=2)
        
        self.light_detector.release()
        self.logger.info("Light monitor stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop (runs in separate thread)"""
        
        while self.running and not self.stop_event.is_set():
            try:
                # Get light reading
                lux, status, metadata = self.light_detector.get_light_level()
                
                self.current_lux = lux
                self.current_status = status
                
                # Add to history
                self._add_to_history(lux, status, metadata)
                
                # Check if we should get AI recommendation
                should_recommend = self._should_get_recommendation(status)
                
                if should_recommend and self.ai_client:
                    # Get AI recommendation (async)
                    try:
                        asyncio.run(self._get_ai_recommendation(lux, status, metadata))
                    except Exception as e:
                        self.logger.error(f"Error getting AI recommendation: {e}")
                
                # Auto-adjust brightness if enabled
                if self.auto_adjust_brightness:
                    self.brightness_control.auto_adjust(lux)
                
                # Notify callback
                if self.callback:
                    self.callback({
                        'lux': lux,
                        'status': status,
                        'metadata': metadata,
                        'recommendation': self.last_recommendation
                    })
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
            
            # Wait for next check
            self.stop_event.wait(self.check_interval)
    
    def _add_to_history(self, lux: float, status: str, metadata: Dict):
        """Add reading to history"""
        
        entry = {
            'timestamp': datetime.now(),
            'lux': lux,
            'status': status,
            'metadata': metadata
        }
        
        self.light_history.append(entry)
        
        # Trim history
        if len(self.light_history) > self.max_history_size:
            self.light_history = self.light_history[-self.max_history_size:]
    
    def _should_get_recommendation(self, status: str) -> bool:
        """Determine if we should get a new AI recommendation"""
        
        # Always recommend for critical conditions
        if status in ['very_low', 'changing']:
            # But not more than once per 5 minutes
            if self.last_warning_time:
                if datetime.now() - self.last_warning_time < timedelta(minutes=5):
                    return False
            
            self.last_warning_time = datetime.now()
            return True
        
        # For other conditions, recommend every 30 minutes
        if self.last_warning_time:
            if datetime.now() - self.last_warning_time < timedelta(minutes=30):
                return False
        
        self.last_warning_time = datetime.now()
        return True
    
    async def _get_ai_recommendation(self, lux: float, status: str, metadata: Dict):
        """Get AI recommendation for current light conditions"""
        
        try:
            light_data = {
                'lux': lux,
                'status': status,
                'metadata': metadata
            }
            
            user_context = {
                'screen_brightness': self.brightness_control.get_brightness() or 'auto',
                'recent_breaks': 0,  # TODO: Get from break manager
                'activity': 'general computer work'
            }
            
            recommendation = await self.ai_client.get_light_recommendation(
                light_data, 
                user_context
            )
            
            self.last_recommendation = recommendation
            
        except Exception as e:
            self.logger.error(f"Failed to get AI recommendation: {e}")
    
    def get_current_status(self) -> Dict:
        """Get current light monitoring status"""
        
        return {
            'lux': self.current_lux,
            'status': self.current_status,
            'running': self.running,
            'auto_adjust': self.auto_adjust_brightness,
            'screen_brightness': self.brightness_control.get_brightness(),
            'last_recommendation': self.last_recommendation
        }
    
    def get_statistics(self) -> Dict:
        """Get light monitoring statistics"""
        
        if not self.light_history:
            return {}
        
        recent = self.light_history[-20:]  # Last 20 readings
        
        lux_values = [entry['lux'] for entry in recent]
        
        return {
            'current': self.current_lux,
            'average': sum(lux_values) / len(lux_values),
            'min': min(lux_values),
            'max': max(lux_values),
            'readings_count': len(self.light_history),
            'status_distribution': self._get_status_distribution(recent)
        }
    
    def _get_status_distribution(self, entries: list) -> Dict:
        """Get distribution of light statuses"""
        
        distribution = {}
        
        for entry in entries:
            status = entry['status']
            distribution[status] = distribution.get(status, 0) + 1
        
        return distribution
    
    def calibrate_camera(self, known_lux: float) -> bool:
        """Calibrate light sensor with known lux value"""
        return self.light_detector.calibrate(known_lux)
    
    def manual_check(self) -> Dict:
        """Perform manual light check (immediate)"""
        
        lux, status, metadata = self.light_detector.get_light_level()
        
        return {
            'lux': lux,
            'status': status,
            'metadata': metadata,
            'screen_brightness': self.brightness_control.get_brightness(),
            'recommended_brightness': self.brightness_control.adjust_for_light(lux)
        }
