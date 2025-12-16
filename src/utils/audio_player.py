"""Audio Player for Notifications"""
import logging
from pathlib import Path
from typing import Optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class AudioPlayer:
    """Simple audio player for notification sounds"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.initialized = False
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.initialized = True
                self.logger.info("Audio player initialized")
            except Exception as e:
                self.logger.warning(f"Could not initialize audio: {e}")
        else:
            self.logger.warning("pygame not available, audio disabled")
    
    def play_sound(self, sound_name: str = "notification"):
        """Play a sound file"""
        if not self.initialized:
            return
        
        try:
            # Look for sound file in assets
            sound_path = Path(__file__).parent.parent / 'assets' / 'sounds' / f'{sound_name}.wav'
            
            if not sound_path.exists():
                # Try mp3
                sound_path = sound_path.with_suffix('.mp3')
            
            if sound_path.exists():
                sound = pygame.mixer.Sound(str(sound_path))
                sound.play()
            else:
                # Play system beep as fallback
                self.logger.debug(f"Sound file not found: {sound_name}")
                self._system_beep()
                
        except Exception as e:
            self.logger.error(f"Error playing sound: {e}")
            self._system_beep()
    
    def _system_beep(self):
        """Fallback system beep"""
        try:
            import winsound
            winsound.Beep(800, 300)  # 800 Hz for 300ms
        except:
            pass
    
    def stop_all(self):
        """Stop all playing sounds"""
        if self.initialized:
            try:
                pygame.mixer.stop()
            except:
                pass
