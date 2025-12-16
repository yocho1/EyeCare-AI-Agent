"""Screen Brightness Control"""
import logging
from typing import Optional

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False


class ScreenBrightness:
    """Manage screen brightness detection and adjustment"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.enabled = SBC_AVAILABLE
        
        if not SBC_AVAILABLE:
            self.logger.info("screen-brightness-control not available. Brightness features disabled.")
    
    def get_brightness(self) -> Optional[int]:
        """
        Get current screen brightness (0-100)
        
        Returns:
            int: Brightness level (0-100), or None if unavailable
        """
        if not self.enabled:
            return None
        
        try:
            brightness = sbc.get_brightness()
            
            # get_brightness() returns a list for multiple monitors
            if isinstance(brightness, list):
                # Return average brightness across all monitors
                if brightness:
                    return int(sum(brightness) / len(brightness))
                return None
            
            return int(brightness)
            
        except Exception as e:
            self.logger.debug(f"Could not get brightness: {e}")
            return None
    
    def set_brightness(self, value: int) -> bool:
        """
        Set screen brightness
        
        Args:
            value: Brightness level (0-100)
        
        Returns:
            bool: True if successful
        """
        if not self.enabled:
            return False
        
        try:
            # Clamp value
            value = max(0, min(100, value))
            sbc.set_brightness(value)
            self.logger.info(f"Screen brightness set to {value}%")
            return True
            
        except Exception as e:
            self.logger.error(f"Could not set brightness: {e}")
            return False
    
    def adjust_for_light(self, ambient_lux: float) -> Optional[int]:
        """
        Calculate recommended screen brightness based on ambient light
        
        Args:
            ambient_lux: Ambient light level in lux
        
        Returns:
            int: Recommended brightness (0-100)
        """
        
        # Brightness recommendations based on ambient light
        # Source: Ergonomics guidelines
        
        if ambient_lux < 50:
            # Very dark - 20-30% brightness
            recommended = 25
        elif ambient_lux < 100:
            # Dark - 30-40% brightness
            recommended = 35
        elif ambient_lux < 200:
            # Dim - 40-50% brightness
            recommended = 45
        elif ambient_lux < 300:
            # Moderate - 50-60% brightness
            recommended = 55
        elif ambient_lux < 500:
            # Optimal - 60-70% brightness
            recommended = 65
        elif ambient_lux < 700:
            # Bright - 70-80% brightness
            recommended = 75
        else:
            # Very bright - 80-90% brightness
            recommended = 85
        
        return recommended
    
    def auto_adjust(self, ambient_lux: float) -> bool:
        """
        Automatically adjust screen brightness based on ambient light
        
        Args:
            ambient_lux: Ambient light level in lux
        
        Returns:
            bool: True if adjustment was made
        """
        recommended = self.adjust_for_light(ambient_lux)
        
        if recommended is None:
            return False
        
        current = self.get_brightness()
        
        if current is None:
            return self.set_brightness(recommended)
        
        # Only adjust if difference is significant (>10%)
        diff = abs(current - recommended)
        if diff > 10:
            return self.set_brightness(recommended)
        
        return False
    
    def fade_to(self, target: int, duration: float = 1.0, steps: int = 10) -> bool:
        """
        Smoothly fade brightness to target value
        
        Args:
            target: Target brightness (0-100)
            duration: Duration in seconds
            steps: Number of steps in the fade
        
        Returns:
            bool: True if successful
        """
        if not self.enabled:
            return False
        
        current = self.get_brightness()
        if current is None:
            return self.set_brightness(target)
        
        import time
        
        step_duration = duration / steps
        step_size = (target - current) / steps
        
        try:
            for i in range(steps):
                new_brightness = int(current + step_size * (i + 1))
                self.set_brightness(new_brightness)
                time.sleep(step_duration)
            
            # Ensure we hit the target exactly
            self.set_brightness(target)
            return True
            
        except Exception as e:
            self.logger.error(f"Error during brightness fade: {e}")
            return False
