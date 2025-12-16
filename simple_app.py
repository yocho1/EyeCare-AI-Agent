"""Simplified EyeCare AI Agent - Minimal Working Version"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import customtkinter as ctk
from src.core.agent import EyeCareAIAgent
from src.utils.config_manager import ConfigManager

# Initialize
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create window
root = ctk.CTk()
root.title("👁️ EyeCare AI Pro")
root.geometry("800x600")

# Make it popup on top
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))

# Load config
config = ConfigManager()

# Create simple UI
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title
title = ctk.CTkLabel(main_frame, text="👁️✨ EyeCare AI Pro ✨👁️", font=("Arial", 28, "bold"))
title.pack(pady=20)

# Status label
status_label = ctk.CTkLabel(main_frame, text="Status: Initializing...", font=("Arial", 16))
status_label.pack(pady=10)

# Info
info_text = """
Welcome to EyeCare AI Agent!

This is a simplified version to ensure the app works.

Features:
• 20-20-20 rule break reminders
• Ambient light detection via webcam
• Eye strain monitoring
• Break notifications

Your break interval: 1 minute (for testing)
"""
info_label = ctk.CTkLabel(main_frame, text=info_text, font=("Arial", 14), justify="left")
info_label.pack(pady=20)

# Initialize agent
print("Initializing agent...")
agent = EyeCareAIAgent(config)

# Start button
def start_monitoring():
    agent.start()
    status_label.configure(text="Status: ✅ Monitoring Active")
    start_btn.configure(state="disabled")
    stop_btn.configure(state="normal")
    print("Monitoring started!")

def stop_monitoring():
    agent.shutdown()
    status_label.configure(text="Status: ⏸️ Stopped")
    start_btn.configure(state="normal")
    stop_btn.configure(state="disabled")
    print("Monitoring stopped!")

def trigger_break():
    print("Manual break triggered!")
    agent.trigger_break_now()

# Buttons
button_frame = ctk.CTkFrame(main_frame)
button_frame.pack(pady=20)

start_btn = ctk.CTkButton(button_frame, text="▶️ Start Monitoring", command=start_monitoring, 
                          width=150, height=40, font=("Arial", 14, "bold"))
start_btn.pack(side="left", padx=10)

stop_btn = ctk.CTkButton(button_frame, text="⏸️ Stop", command=stop_monitoring,
                         width=150, height=40, font=("Arial", 14, "bold"), state="disabled")
stop_btn.pack(side="left", padx=10)

break_btn = ctk.CTkButton(button_frame, text="💆 Take Break Now", command=trigger_break,
                          width=150, height=40, font=("Arial", 14, "bold"))
break_btn.pack(side="left", padx=10)

# Countdown label
countdown_label = ctk.CTkLabel(main_frame, text="Next break in: Not started", font=("Arial", 14))
countdown_label.pack(pady=20)

def update_countdown():
    if agent.scheduler and agent.scheduler.running:
        remaining = agent.scheduler.get_time_until_break()
        if remaining:
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            countdown_label.configure(text=f"Next break in: {mins:02d}:{secs:02d}")
        else:
            countdown_label.configure(text="Next break in: --:--")
    root.after(1000, update_countdown)

update_countdown()

# Close handler
def on_close():
    print("Closing application...")
    agent.shutdown()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

print("✅ Window created! Starting main loop...")
root.mainloop()
print("Application closed.")
