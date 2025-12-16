"""Main EyeCare AI Agent - Orchestrates all components"""
import logging
import asyncio
from typing import Optional, Dict, Callable
from datetime import datetime

from .scheduler import BreakScheduler
from .notifier import Notifier
from .analytics import Analytics
from ..ai.openrouter_client import OpenRouterClient
from ..hardware.light_monitor import LightMonitor


class EyeCareAIAgent:
    """Main agent that orchestrates all eye care features"""
    
    def __init__(self, config_manager):
        """
        Initialize the EyeCare AI Agent
        
        Args:
            config_manager: ConfigManager instance
        """
        self.logger = logging.getLogger(__name__)
        self.config = config_manager
        
        # State
        self.running = False
        self.paused = False
        
        # UI callback
        self.ui_update_callback: Optional[Callable] = None
        
        # Initialize AI client
        self.logger.info("Initializing AI client...")
        api_key = self.config.get_api_key()
        model = self.config.get_model()
        self.ai_client = OpenRouterClient(api_key, model)
        
        # Initialize analytics
        self.logger.info("Initializing analytics...")
        analytics_config = {
            'enabled': self.config.get('analytics.enabled', True),
            'track_screen_time': self.config.get('analytics.track_screen_time', True),
            'track_break_compliance': self.config.get('analytics.track_break_compliance', True),
            'track_light_conditions': self.config.get('analytics.track_light_conditions', True)
        }
        self.analytics = Analytics(analytics_config)
        
        # Initialize notifier
        self.logger.info("Initializing notifier...")
        notifier_config = {
            'show_notifications': self.config.get('ui_settings.show_notifications', True),
            'break_sound_enabled': self.config.get('break_settings.break_sound_enabled', True),
            'notification_duration_seconds': self.config.get('ui_settings.notification_duration_seconds', 10)
        }
        self.notifier = Notifier(notifier_config)
        
        # Initialize break scheduler
        self.logger.info("Initializing break scheduler...")
        break_config = {
            'work_interval_minutes': self.config.get('break_settings.work_interval_minutes', 20),
            'break_duration_seconds': self.config.get('break_settings.break_duration_seconds', 20),
            'enable_breaks': self.config.get('break_settings.enable_breaks', True),
            'auto_pause_on_idle': self.config.get('break_settings.auto_pause_on_idle', True),
            'idle_threshold_minutes': self.config.get('break_settings.idle_threshold_minutes', 5)
        }
        self.scheduler = BreakScheduler(break_config, self._on_break_due)
        
        # Initialize light monitor (can be disabled in config)
        self.logger.info("Initializing light monitor...")
        light_enabled = self.config.get('light_monitoring.enabled', True)
        light_config = {
            'enabled': light_enabled,
            'camera_index': self.config.get('light_monitoring.camera_index', 0),
            'check_interval_seconds': self.config.get('light_monitoring.check_interval_seconds', 30),
            'auto_adjust_brightness': self.config.get('light_monitoring.auto_adjust_brightness', False)
        }
        if light_enabled:
            self.light_monitor = LightMonitor(light_config, self.ai_client, self._on_light_update)
            self.logger.info("Light monitor enabled")
        else:
            self.light_monitor = None
            self.logger.info("Light monitor disabled via config")
        
        self.logger.info("✓ EyeCare AI Agent initialized successfully")
    
    def start(self):
        """Start the agent and all subsystems"""
        
        if self.running:
            self.logger.warning("Agent already running")
            return
        
        self.logger.info("🚀 Starting EyeCare AI Agent...")
        self.running = True
        
        # Start subsystems
        self.scheduler.start()
        if self.light_monitor:
            self.light_monitor.start()
        
        # Test notification
        self.notifier.test_notification()
        
        self.logger.info("✓ EyeCare AI Agent started successfully")
    
    def shutdown(self):
        """Shutdown the agent and all subsystems"""
        
        if not self.running:
            return
        
        self.logger.info("Shutting down EyeCare AI Agent...")
        self.running = False
        
        # Stop subsystems
        self.scheduler.stop()
        if self.light_monitor:
            self.light_monitor.stop()
        
        # End analytics session
        self.analytics.end_session()
        
        self.logger.info("✓ EyeCare AI Agent shutdown complete")
    
    def pause(self, duration_seconds: Optional[int] = None):
        """
        Pause the agent
        
        Args:
            duration_seconds: If provided, pause for this duration. Otherwise pause indefinitely.
        """
        
        self.paused = True
        self.scheduler.pause(duration_seconds)
        
        if duration_seconds:
            self.logger.info(f"Agent paused for {duration_seconds} seconds")
            self.notifier.show_info(
                "EyeCare AI Paused",
                f"Break reminders paused for {duration_seconds // 60} minutes"
            )
        else:
            self.logger.info("Agent paused indefinitely")
            self.notifier.show_info(
                "EyeCare AI Paused",
                "Break reminders are paused"
            )
    
    def resume(self):
        """Resume the agent"""
        
        self.paused = False
        self.scheduler.resume()
        
        self.logger.info("Agent resumed")
        self.notifier.show_info(
            "EyeCare AI Resumed",
            "Break reminders are active"
        )
    
    def trigger_break_now(self):
        """Manually trigger a break immediately"""
        
        self.scheduler.trigger_break_now()
    
    def record_break_completed(self):
        """Record that user completed a break"""
        
        self.scheduler.break_completed()
        self.analytics.record_break_completed()
        
        # Show encouragement
        self.notifier.show_achievement(
            "Great job taking a break! Your eyes thank you. 👁️✨"
        )
    
    def record_break_skipped(self):
        """Record that user skipped a break"""
        
        self.scheduler.break_skipped()
        self.analytics.record_break_skipped()
    
    def _on_break_due(self, data: Dict):
        """Callback when break is due"""
        
        self.logger.info(">>> BREAK DUE CALLBACK TRIGGERED <<<")
        
        # Record analytics
        self.analytics.record_break_offered()
        
        # Show notification
        self.notifier.show_break_reminder(data)
        
        # Update UI if callback is set
        if self.ui_update_callback:
            self.logger.info("UI callback is set, calling it now...")
            try:
                self.ui_update_callback({
                    'type': 'break_due',
                    'data': data
                })
                self.logger.info("UI callback completed successfully")
            except RuntimeError as e:
                if "main thread is not in main loop" in str(e):
                    self.logger.debug(f"UI not ready yet: {e}")
                else:
                    self.logger.error(f"Error in UI callback: {e}")
            except Exception as e:
                self.logger.error(f"Error in UI callback: {e}", exc_info=True)
        else:
            self.logger.warning("UI callback is NOT set!")
    
    def _on_light_update(self, data: Dict):
        """Callback when light conditions change"""
        
        lux = data.get('lux', 0)
        status = data.get('status', 'unknown')
        recommendation = data.get('recommendation')
        
        # Record analytics
        self.analytics.record_light_reading(lux, status)
        
        # Show warning for critical conditions
        if status in ['very_low', 'high'] and recommendation:
            self.notifier.show_light_warning(
                lux, 
                status, 
                recommendation.recommendation if recommendation else "Adjust lighting"
            )
        
        # Update UI if callback is set
        if self.ui_update_callback:
            try:
                self.ui_update_callback({
                    'type': 'light_update',
                    'data': data
                })
            except Exception as e:
                self.logger.error(f"Error in UI callback: {e}")
    
    def set_ui_callback(self, callback: Callable):
        """Set callback for UI updates"""
        self.ui_update_callback = callback
    
    def get_status(self) -> Dict:
        """Get comprehensive agent status"""
        
        scheduler_status = self.scheduler.get_status()
        light_status = self.light_monitor.get_current_status() if self.light_monitor else {
            'running': False,
            'status': 'disabled'
        }
        today_stats = self.analytics.get_today_statistics()
        
        return {
            'agent': {
                'running': self.running,
                'paused': self.paused
            },
            'scheduler': scheduler_status,
            'light': light_status,
            'today': today_stats,
            'ai': {
                'enabled': self.ai_client.enabled,
                'model': self.ai_client.model
            }
        }
    
    def get_statistics(self) -> Dict:
        """Get detailed statistics"""
        
        return {
            'scheduler': self.scheduler.get_statistics(),
            'light': self.light_monitor.get_statistics() if self.light_monitor else {},
            'today': self.analytics.get_today_statistics(),
            'weekly': self.analytics.get_weekly_summary()
        }
    
    def get_ai_recommendation(self, query: str) -> str:
        """Get AI recommendation for a query"""
        
        try:
            # This would need to be made async properly
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            recommendation = loop.run_until_complete(
                self.ai_client.get_break_recommendation(
                    time_since_break=20,
                    strain_level="medium",
                    light_status=self.light_monitor.current_status
                )
            )
            
            loop.close()
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Error getting AI recommendation: {e}")
            return "Take a 20-second break and look at something 20 feet away."
    
    def manual_light_check(self) -> Dict:
        """Perform manual light check"""
        if not self.light_monitor:
            return {'status': 'disabled', 'lux': 0, 'recommended_brightness': 0}
        return self.light_monitor.manual_check()
    
    def calibrate_light_sensor(self, known_lux: float) -> bool:
        """Calibrate light sensor with known value"""
        if not self.light_monitor:
            return False
        return self.light_monitor.calibrate_camera(known_lux)
    
    def export_analytics(self) -> str:
        """Export analytics data"""
        return self.analytics.export_data()
    
    def update_settings(self, **settings):
        """Update agent settings"""
        
        # Update break settings
        if any(k.startswith('break_') for k in settings):
            break_settings = {
                k.replace('break_', ''): v 
                for k, v in settings.items() 
                if k.startswith('break_')
            }
            self.scheduler.update_settings(**break_settings)
        
        # Save to config
        for key, value in settings.items():
            self.config.set(key, value)
        
        self.logger.info(f"Settings updated: {settings}")
