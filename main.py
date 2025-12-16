"""
EyeCare AI Agent - Main Entry Point

A professional eye care application with AI-powered recommendations,
ambient light detection, and intelligent break scheduling.
"""
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    print("ERROR: customtkinter not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

from src.core.agent import EyeCareAIAgent
from src.ui.main_window import MainWindow
from src.ui.system_tray import SystemTrayIcon
from src.utils.config_manager import ConfigManager
from src.utils.theme_manager import ThemeManager


def setup_logging():
    """Professional logging setup"""
    
    # Create logs directory
    log_dir = Path.home() / '.eyecare_agent' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create log file
    log_file = log_dir / f'eyecare_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("EyeCare AI Agent Starting...")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)


class EyeCareAIApplication:
    """Main application controller following Clean Architecture"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing EyeCare AI Application")
        
        # Load configuration
        self.config = ConfigManager()
        
        # Initialize theme
        theme = self.config.get('ui_settings.theme', 'dark')
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("👁️ EyeCare AI Pro")
        
        # Get window size from config
        width = self.config.get('ui_settings.window_width', 900)
        height = self.config.get('ui_settings.window_height', 700)
        self.root.geometry(f"{width}x{height}")
        
        # Force window to appear on top and in front
        self.root.update()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.after(500, lambda: self.root.attributes('-topmost', False))
        
        # Center window
        self._center_window()
        
        # Initialize core components
        self.logger.info("Initializing core components...")
        self.agent = EyeCareAIAgent(self.config)
        
        self.logger.info("Creating main window UI...")
        try:
            self.ui = MainWindow(self.root, self.agent, self.config)
            self.logger.info("✓ Main window UI created")
        except Exception as e:
            self.logger.error(f"Failed to create main window: {e}", exc_info=True)
            raise
        
        # Setup system tray
        self.tray_icon = None
        if self.config.get('app_settings.minimize_to_tray', True):
            self._setup_system_tray()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.logger.info("✓ Application initialized successfully")
    
    def _center_window(self):
        """Center window on screen"""
        
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - self.root.winfo_width()) // 2
        y = (screen_height - self.root.winfo_height()) // 2
        
        self.root.geometry(f"+{x}+{y}")
    
    def _setup_system_tray(self):
        """Setup system tray icon with light status"""
        
        try:
            self.tray_icon = SystemTrayIcon(
                icon_path=None,  # Will use default icon
                tooltip="EyeCare AI Agent",
                menu_options={
                    "Show Dashboard": self.show_window,
                    "Pause for 1 hour": lambda: self.agent.pause(3600),
                    "Take Break Now": self.agent.trigger_break_now,
                    "Light Analysis": self.show_light_analysis,
                    "Exit": self.quit_application
                }
            )
            self.logger.info("✓ System tray icon created")
        except Exception as e:
            self.logger.warning(f"Could not create system tray icon: {e}")
            self.tray_icon = None
    
    def show_light_analysis(self):
        """Show light analysis panel"""
        
        self.ui.show_panel("light_analysis")
        self.root.deiconify()  # Restore window if minimized
    
    def show_window(self):
        """Show main window"""
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def on_closing(self):
        """Handle window closing event"""
        
        if self.config.get('app_settings.minimize_to_tray', True) and self.tray_icon:
            # Minimize to tray
            self.root.withdraw()
            self.logger.info("Application minimized to tray")
        else:
            # Quit application
            self.quit_application()
    
    def quit_application(self):
        """Clean shutdown"""
        
        self.logger.info("Shutting down EyeCare AI Application...")
        
        try:
            # Shutdown agent
            self.agent.shutdown()
            
            # Shutdown tray icon
            if self.tray_icon:
                self.tray_icon.shutdown()
            
            # Quit GUI
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        
        self.logger.info("✓ Application shutdown complete")
        sys.exit(0)
    
    def run(self):
        """Start the application"""
        
        self.logger.info("🚀 Starting EyeCare AI Application")
        
        try:
            # Make sure window is visible
            self.root.update()
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            # Start background services
            self.agent.start()
            
            # Start UI mainloop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            self.quit_application()
        except Exception as e:
            self.logger.critical(f"Application error: {e}", exc_info=True)
            raise


def check_dependencies():
    """Check if required dependencies are installed"""
    
    missing = []
    
    # Check critical dependencies
    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")
    
    try:
        import PIL
    except ImportError:
        missing.append("Pillow")
    
    if missing:
        print("\n❌ Missing required dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        print()
        return False
    
    return True


def print_banner():
    """Print application banner"""
    
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           EyeCare AI Agent Pro - Starting                ║
    ║                                                           ║
    ║         Intelligent Eye Care with AI & Light Monitoring  ║
    ║                                                           ║
    ║                      Version 1.0.0                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    try:
        print(banner)
    except:
        print("EyeCare AI Agent Pro - Starting...")


def main():
    """Application entry point with exception handling"""
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    logger = logging.getLogger(__name__)
    
    try:
        # Create and run application
        app = EyeCareAIApplication()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
        logger.info("Application terminated by user")
        sys.exit(0)
        
    except Exception as e:
        logger.critical(f"Application failed: {e}", exc_info=True)
        
        # Show error dialog
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showerror(
                "Critical Error",
                f"EyeCare AI encountered a critical error:\n\n{str(e)}\n\n"
                "Please check the log file for details.\n\n"
                f"Log location: {Path.home() / '.eyecare_agent' / 'logs'}"
            )
        except:
            print(f"\n❌ Critical Error: {e}")
            print(f"\nCheck logs at: {Path.home() / '.eyecare_agent' / 'logs'}")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
