"""Quick test of the break modal"""
import customtkinter as ctk
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create main window
root = ctk.CTk()
root.title("Modal Test")
root.geometry("400x300")

def show_modal():
    """Show break modal"""
    try:
        logger.info("=== BREAK MODAL START ===")
        
        # Create modal
        modal = ctk.CTkToplevel(root)
        modal.title("Break Time!")
        modal.geometry("500x450")
        
        logger.info("✓ Modal window created")
        
        # Make it stay on top
        modal.attributes('-topmost', True)
        modal.lift()
        modal.focus_force()
        
        logger.info("✓ Modal focused")
        
        # Title
        title = ctk.CTkLabel(
            modal,
            text="TAKE A BREAK",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#FF6B6B"
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            modal,
            text="Look away from the screen\nFocus on something 20 feet away\nFor 20 seconds",
            font=ctk.CTkFont(size=14),
            justify="center",
            text_color="#CCCCCC"
        )
        instructions.pack(pady=15)
        
        # Countdown
        countdown_label = ctk.CTkLabel(
            modal,
            text="20",
            font=ctk.CTkFont(size=80, weight="bold"),
            text_color="#4CAF50"
        )
        countdown_label.pack(pady=30)
        
        # Status
        status_label = ctk.CTkLabel(
            modal,
            text="seconds remaining",
            font=ctk.CTkFont(size=14),
            text_color="#AAAAAA"
        )
        status_label.pack()
        
        logger.info("✓ Modal UI created")
        
        # Skip button
        def skip_break():
            logger.info("Break skipped")
            modal.destroy()
        
        skip_btn = ctk.CTkButton(
            modal,
            text="Skip Break",
            command=skip_break,
            width=200,
            height=45,
            fg_color="gray"
        )
        skip_btn.pack(pady=20)
        
        # Countdown
        countdown = [20]
        
        def update_countdown():
            try:
                countdown[0] -= 1
                countdown_label.configure(text=str(countdown[0]))
                
                if countdown[0] > 0:
                    root.after(1000, update_countdown)
                else:
                    logger.info("✓ Break completed")
                    countdown_label.configure(text="✓")
                    status_label.configure(text="Break complete!")
                    root.after(1000, lambda: modal.destroy())
            except Exception as e:
                logger.error(f"Countdown error: {e}", exc_info=True)
                modal.destroy()
        
        modal.protocol("WM_DELETE_WINDOW", skip_break)
        
        logger.info("✓ Starting countdown")
        root.after(500, update_countdown)
        
        logger.info("=== BREAK MODAL COMPLETE ===")
        
    except Exception as e:
        logger.error(f"❌ MODAL FAILED: {e}", exc_info=True)

# Test button
btn = ctk.CTkButton(root, text="Test Modal", command=show_modal)
btn.pack(pady=20)

logger.info("Starting test app...")
root.mainloop()
logger.info("Test app closed")
