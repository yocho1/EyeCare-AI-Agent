"""Smart Notification System"""
import logging
from typing import Optional, Dict
from datetime import datetime

try:
    from plyer import notification as plyer_notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

from ..utils.audio_player import AudioPlayer


class Notifier:
    """Smart notification system for break reminders"""
    
    def __init__(self, config: dict):
        """
        Initialize notifier
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Settings
        self.enabled = config.get('show_notifications', True)
        self.sound_enabled = config.get('break_sound_enabled', True)
        self.duration = config.get('notification_duration_seconds', 10)
        
        # Audio player
        self.audio_player = AudioPlayer()
        
        # Check notification availability
        self.system_notifications_available = PLYER_AVAILABLE
        
        if not self.system_notifications_available:
            self.logger.warning("System notifications not available (plyer not installed)")
        
        self.logger.info("Notifier initialized")
    
    def show_break_reminder(self, data: Optional[Dict] = None):
        """Show break reminder notification"""
        
        if not self.enabled:
            return
        
        title = "👁️ Eye Care Break Time!"
        message = "Take a 20-second break using the 20-20-20 rule:\nLook at something 20 feet away."
        
        if data:
            breaks_today = data.get('breaks_today', 0)
            if breaks_today > 0:
                message += f"\n\nBreaks today: {breaks_today}"
        
        self._show_notification(title, message, urgency='normal')
        
        # Play sound
        if self.sound_enabled:
            self.audio_player.play_sound('break_reminder')
    
    def show_light_warning(self, lux: float, status: str, recommendation: str):
        """Show lighting condition warning"""
        
        if not self.enabled:
            return
        
        icons = {
            'very_low': '🔴',
            'low': '🟡',
            'optimal': '🟢',
            'high': '🟣',
            'changing': '🔵'
        }
        
        icon = icons.get(status, '💡')
        
        title = f"{icon} Lighting Alert"
        
        if status == 'very_low':
            message = f"Very low light detected ({lux:.0f} lux)\n{recommendation}"
            urgency = 'critical'
        elif status == 'low':
            message = f"Low light detected ({lux:.0f} lux)\n{recommendation}"
            urgency = 'normal'
        elif status == 'high':
            message = f"Very bright light ({lux:.0f} lux)\n{recommendation}"
            urgency = 'normal'
        else:
            message = f"Light level: {lux:.0f} lux\n{recommendation}"
            urgency = 'low'
        
        self._show_notification(title, message, urgency=urgency)
        
        # Play sound for critical warnings
        if urgency == 'critical' and self.sound_enabled:
            self.audio_player.play_sound('warning')
    
    def show_eye_strain_alert(self, message: str):
        """Show eye strain alert"""
        
        if not self.enabled:
            return
        
        title = "⚠️ Eye Strain Alert"
        
        self._show_notification(title, message, urgency='normal')
        
        if self.sound_enabled:
            self.audio_player.play_sound('alert')
    
    def show_achievement(self, message: str):
        """Show achievement notification"""
        
        if not self.enabled:
            return
        
        title = "🎉 Well Done!"
        
        self._show_notification(title, message, urgency='low')
        
        if self.sound_enabled:
            self.audio_player.play_sound('achievement')
    
    def show_info(self, title: str, message: str):
        """Show general information notification"""
        
        if not self.enabled:
            return
        
        self._show_notification(title, message, urgency='low')
    
    def _show_notification(self, title: str, message: str, urgency: str = 'normal'):
        """
        Show system notification
        
        Args:
            title: Notification title
            message: Notification message
            urgency: 'low', 'normal', or 'critical'
        """
        
        if not self.system_notifications_available:
            # Fallback: Log the notification
            self.logger.info(f"NOTIFICATION: {title} - {message}")
            return
        
        try:
            # Truncate message if too long
            if len(message) > 250:
                message = message[:247] + "..."
            
            plyer_notification.notify(
                title=title,
                message=message,
                app_name='EyeCare AI Agent',
                app_icon=None,  # You can set path to icon
                timeout=self.duration,
                ticker='EyeCare AI'
            )
            
            self.logger.debug(f"Notification shown: {title}")
            
        except Exception as e:
            self.logger.error(f"Failed to show notification: {e}")
    
    def test_notification(self):
        """Test notification system"""
        
        self.show_info(
            "EyeCare AI Agent",
            "Notification system is working correctly! ✓"
        )
        
        if self.sound_enabled:
            self.audio_player.play_sound('notification')
