"""System Tray Icon"""
import logging
from typing import Dict, Callable
import os
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False


class SystemTrayIcon:
    """System tray icon for background operation"""
    
    def __init__(self, 
                 icon_path: str = None,
                 tooltip: str = "EyeCare AI Agent",
                 menu_options: Dict[str, Callable] = None):
        """
        Initialize system tray icon
        
        Args:
            icon_path: Path to icon file
            tooltip: Tooltip text
            menu_options: Dictionary of menu items and their callbacks
        """
        self.logger = logging.getLogger(__name__)
        self.tooltip = tooltip
        self.menu_options = menu_options or {}
        
        if not TRAY_AVAILABLE:
            self.logger.warning("pystray not available. System tray disabled.")
            self.icon = None
            return
        
        # Load or create icon
        if icon_path and Path(icon_path).exists():
            try:
                self.image = Image.open(icon_path)
            except:
                self.image = self._create_default_icon()
        else:
            self.image = self._create_default_icon()
        
        # Create menu
        menu = self._create_menu()
        
        # Create icon
        self.icon = pystray.Icon(
            "eyecare_agent",
            self.image,
            tooltip,
            menu
        )
        
        # Start in background thread
        import threading
        self.thread = threading.Thread(target=self._run_icon, daemon=True)
        self.thread.start()
        
        self.logger.info("System tray icon created")
    
    def _create_default_icon(self) -> Image:
        """Create a default icon image"""
        
        # Create a simple eye icon
        size = 64
        image = Image.new('RGB', (size, size), color='#1f6feb')
        draw = ImageDraw.Draw(image)
        
        # Draw eye shape
        draw.ellipse([10, 20, 54, 44], fill='white', outline='black', width=2)
        draw.ellipse([24, 26, 40, 38], fill='#1f6feb', outline='black', width=2)
        
        return image
    
    def _create_menu(self):
        """Create tray menu"""
        
        if not TRAY_AVAILABLE:
            return None
        
        from pystray import Menu, MenuItem
        
        items = []
        
        for label, callback in self.menu_options.items():
            items.append(MenuItem(label, callback))
        
        return Menu(*items)
    
    def _run_icon(self):
        """Run the icon (blocking call)"""
        
        if self.icon:
            try:
                self.icon.run()
            except Exception as e:
                self.logger.error(f"Error running tray icon: {e}")
    
    def update_tooltip(self, text: str):
        """Update tooltip text"""
        
        if self.icon:
            self.icon.title = text
    
    def shutdown(self):
        """Shutdown the tray icon"""
        
        if self.icon:
            try:
                self.icon.stop()
                self.logger.info("System tray icon stopped")
            except:
                pass
