"""Ambient Light Detection using Webcam"""
import logging
from typing import Tuple, Optional, Dict
from datetime import datetime
import numpy as np

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


class AmbientLightDetector:
    """Professional light detection using webcam and algorithms"""
    
    # Light classification thresholds (lux)
    THRESHOLDS = {
        'very_low': (0, 100),
        'low': (100, 200),
        'optimal': (300, 500),
        'high': (500, 1000),
        'very_high': (1000, float('inf'))
    }
    
    def __init__(self, camera_index: int = 0):
        self.logger = logging.getLogger(__name__)
        self.camera_index = camera_index
        self.cap = None
        self.enabled = CV2_AVAILABLE
        self.calibration_factor = 1.0  # Adjust based on camera
        self.last_reading = None
        
        if not CV2_AVAILABLE:
            self.logger.warning("OpenCV not available. Light detection will use fallback methods.")
    
    def initialize(self) -> bool:
        """Initialize camera with error handling"""
        if not self.enabled:
            return False
        
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)  # DirectShow on Windows
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            if not self.cap.isOpened():
                self.logger.warning("Could not open webcam. Using fallback light detection.")
                return False
            
            # Test capture
            ret, _ = self.cap.read()
            if not ret:
                self.logger.warning("Could not capture frame. Using fallback light detection.")
                self.cap.release()
                self.cap = None
                return False
            
            self.logger.info(f"Camera initialized successfully (index: {self.camera_index})")
            return True
            
        except Exception as e:
            self.logger.error(f"Camera initialization failed: {e}")
            self.cap = None
            return False
    
    def get_light_level(self) -> Tuple[float, str, Dict]:
        """
        Get current ambient light level
        
        Returns:
            (lux_estimate, status, metadata)
        """
        if self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if ret:
                    return self._analyze_frame(frame)
            except Exception as e:
                self.logger.error(f"Error capturing frame: {e}")
        
        # Fallback: Use time-based estimation
        return self._estimate_light_fallback()
    
    def _analyze_frame(self, frame) -> Tuple[float, str, Dict]:
        """Analyze webcam frame for light estimation"""
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate image statistics
        mean_brightness = np.mean(gray)
        std_brightness = np.std(gray)
        median_brightness = np.median(gray)
        
        # Calculate histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_normalized = hist.flatten() / hist.sum()
        
        # Detect overexposed areas (potential light sources)
        _, overexposed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        overexposed_ratio = np.sum(overexposed > 0) / overexposed.size
        
        # Detect underexposed areas
        _, underexposed = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        underexposed_ratio = np.sum(underexposed > 0) / underexposed.size
        
        # Convert pixel brightness to lux estimate
        # This is a simplified model - real calibration needed for accuracy
        lux_estimate = self._pixel_to_lux(
            mean_brightness, 
            std_brightness,
            overexposed_ratio,
            underexposed_ratio
        )
        
        # Apply calibration factor
        lux_estimate *= self.calibration_factor
        
        # Classify light level
        status = self._classify_light_level(lux_estimate, overexposed_ratio, std_brightness)
        
        # Build metadata
        metadata = {
            'mean_brightness': float(mean_brightness),
            'std_brightness': float(std_brightness),
            'median_brightness': float(median_brightness),
            'overexposed_ratio': float(overexposed_ratio),
            'underexposed_ratio': float(underexposed_ratio),
            'contrast': float(std_brightness),
            'frame_size': frame.shape,
            'timestamp': datetime.now().isoformat(),
            'source': 'webcam',
            'camera_index': self.camera_index
        }
        
        self.last_reading = (lux_estimate, status, metadata)
        return lux_estimate, status, metadata
    
    def _pixel_to_lux(self, 
                     mean: float, 
                     std: float,
                     overexposed: float,
                     underexposed: float) -> float:
        """
        Convert pixel brightness to lux estimate
        
        This is a simplified empirical model. For accurate readings,
        calibration with a real lux meter is needed.
        
        Typical indoor lighting:
        - 50-100 lux: Dark room
        - 200-300 lux: Normal room lighting
        - 400-500 lux: Bright office lighting
        - 500-1000 lux: Very bright room
        - 1000+ lux: Direct sunlight (indoors near window)
        """
        
        # Base conversion (empirical)
        # Typical webcams have different sensitivities, this is a middle-ground estimate
        base_lux = (mean / 255.0) * 800
        
        # Adjust for contrast (high contrast = more directional light)
        contrast_factor = 1.0 + (std / 100.0)
        
        # Adjust for overexposure (bright light sources present)
        if overexposed > 0.1:  # More than 10% overexposed
            base_lux *= (1.0 + overexposed * 2.0)
        
        # Adjust for underexposure (very dark conditions)
        if underexposed > 0.5:  # More than 50% underexposed
            base_lux *= 0.5
        
        # Apply contrast factor
        estimated_lux = base_lux * contrast_factor
        
        # Clamp to reasonable range
        return max(10, min(estimated_lux, 2000))
    
    def _classify_light_level(self, lux: float, overexposed_ratio: float, contrast: float) -> str:
        """
        Classify light conditions based on lux and image characteristics
        
        Returns: 'optimal', 'low', 'very_low', 'high', 'changing'
        """
        
        # Check for rapidly changing light (high contrast with overexposure)
        if contrast > 60 and overexposed_ratio > 0.2:
            return 'changing'
        
        # Check for very bright conditions
        if lux > 1000 or overexposed_ratio > 0.3:
            return 'high'
        
        # Check for optimal range
        if 300 <= lux <= 500:
            return 'optimal'
        
        # Check for suboptimal but acceptable
        if 200 <= lux < 300 or 500 < lux <= 700:
            return 'low' if lux < 300 else 'high'
        
        # Check for very low light
        if lux < 100:
            return 'very_low'
        
        # Default to low for anything else
        return 'low' if lux < 300 else 'high'
    
    def _estimate_light_fallback(self) -> Tuple[float, str, Dict]:
        """
        Fallback light estimation based on time of day and screen brightness
        
        Used when camera is not available
        """
        
        now = datetime.now()
        hour = now.hour
        
        # Time-based estimation
        if 6 <= hour < 8:  # Early morning
            lux = 150
            status = 'low'
        elif 8 <= hour < 10:  # Morning
            lux = 300
            status = 'optimal'
        elif 10 <= hour < 16:  # Midday
            lux = 450
            status = 'optimal'
        elif 16 <= hour < 18:  # Late afternoon
            lux = 300
            status = 'optimal'
        elif 18 <= hour < 20:  # Evening
            lux = 200
            status = 'low'
        else:  # Night
            lux = 80
            status = 'very_low'
        
        # Try to get screen brightness for better estimation
        try:
            from .screen_brightness import ScreenBrightness
            brightness_mgr = ScreenBrightness()
            screen_brightness = brightness_mgr.get_brightness()
            
            if screen_brightness is not None:
                # If screen is very bright at night, assume lights are on
                if hour >= 20 or hour < 6:
                    if screen_brightness > 70:
                        lux = 250
                        status = 'low'
        except:
            pass
        
        metadata = {
            'lux': lux,
            'source': 'time_based_fallback',
            'hour': hour,
            'timestamp': datetime.now().isoformat(),
            'note': 'Camera not available, using time-based estimation'
        }
        
        return lux, status, metadata
    
    def calibrate(self, known_lux_value: float):
        """
        Calibrate the sensor with a known light source
        
        Steps:
        1. Place a calibrated lux meter next to the camera
        2. Note the actual lux reading
        3. Call this method with that value
        4. The camera will adjust its conversion factor
        """
        
        if not self.cap or not self.cap.isOpened():
            self.logger.error("Camera not initialized. Cannot calibrate.")
            return False
        
        # Get current reading
        current_lux, _, _ = self.get_light_level()
        
        if current_lux > 0:
            # Calculate calibration factor
            self.calibration_factor = known_lux_value / current_lux
            self.logger.info(f"Calibrated: factor = {self.calibration_factor:.2f}")
            self.logger.info(f"Before: {current_lux:.0f} lux, Target: {known_lux_value:.0f} lux")
            return True
        
        return False
    
    def get_last_reading(self) -> Optional[Tuple[float, str, Dict]]:
        """Get the last light reading without capturing a new frame"""
        return self.last_reading
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            try:
                self.cap.release()
                self.logger.info("Camera released")
            except:
                pass
            self.cap = None
    
    def __del__(self):
        """Cleanup on destruction"""
        self.release()
