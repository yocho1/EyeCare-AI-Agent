"""Ultra Minimal EyeCare AI - No Freezing"""
import customtkinter as ctk

# Create window
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("👁️ EyeCare AI Pro")
root.geometry("600x400")

# Force to front
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))

# Main frame
frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=30, pady=30)

# Title
title = ctk.CTkLabel(frame, text="👁️✨ EyeCare AI Pro ✨👁️", 
                     font=("Arial", 32, "bold"))
title.pack(pady=30)

# Status
status = ctk.CTkLabel(frame, text="Ready to protect your eyes!", 
                      font=("Arial", 18))
status.pack(pady=20)

# Timer display
timer_label = ctk.CTkLabel(frame, text="00:00", 
                           font=("Arial", 48, "bold"))
timer_label.pack(pady=20)

# Variables
seconds_left = 60  # 1 minute
monitoring = False

def update_timer():
    global seconds_left, monitoring
    
    if monitoring and seconds_left > 0:
        seconds_left -= 1
        mins = seconds_left // 60
        secs = seconds_left % 60
        timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        
        if seconds_left == 0:
            show_break()
    
    root.after(1000, update_timer)

def start_monitoring():
    global monitoring, seconds_left
    monitoring = True
    seconds_left = 60  # Reset to 1 minute
    status.configure(text="✅ Monitoring Active - Break in 1 minute")
    start_btn.configure(state="disabled")
    stop_btn.configure(state="normal")

def stop_monitoring():
    global monitoring
    monitoring = False
    status.configure(text="⏸️ Monitoring Paused")
    start_btn.configure(state="normal")
    stop_btn.configure(state="disabled")

def show_break():
    global monitoring, seconds_left
    monitoring = False
    seconds_left = 60
    
    # Create break window
    break_win = ctk.CTkToplevel(root)
    break_win.title("Break Time!")
    break_win.geometry("400x300")
    break_win.lift()
    break_win.attributes('-topmost', True)
    
    ctk.CTkLabel(break_win, text="⏰ Time for a Break!", 
                font=("Arial", 24, "bold")).pack(pady=20)
    
    ctk.CTkLabel(break_win, text="Look at something 20 feet away\nfor 20 seconds", 
                font=("Arial", 16)).pack(pady=20)
    
    countdown = [20]
    count_label = ctk.CTkLabel(break_win, text="20", font=("Arial", 48, "bold"))
    count_label.pack(pady=20)
    
    def update_break():
        countdown[0] -= 1
        count_label.configure(text=str(countdown[0]))
        if countdown[0] > 0:
            break_win.after(1000, update_break)
        else:
            break_win.destroy()
            start_monitoring()
    
    break_win.after(1000, update_break)
    
    def skip():
        break_win.destroy()
        start_monitoring()
    
    ctk.CTkButton(break_win, text="Skip", command=skip).pack(pady=10)

# Buttons
btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
btn_frame.pack(pady=20)

start_btn = ctk.CTkButton(btn_frame, text="▶️ Start", command=start_monitoring,
                         width=120, height=40, font=("Arial", 16, "bold"))
start_btn.pack(side="left", padx=10)

stop_btn = ctk.CTkButton(btn_frame, text="⏸️ Stop", command=stop_monitoring,
                        width=120, height=40, font=("Arial", 16, "bold"),
                        state="disabled")
stop_btn.pack(side="left", padx=10)

break_now_btn = ctk.CTkButton(btn_frame, text="💆 Break Now", command=show_break,
                             width=120, height=40, font=("Arial", 16, "bold"))
break_now_btn.pack(side="left", padx=10)

# Start timer
update_timer()

print("✅ Window is now visible!")
print("👁️ Click 'Start' to begin 1-minute break reminders")

root.mainloop()
print("Application closed")
