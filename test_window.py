"""Quick test to see if CTk window works"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import customtkinter as ctk

print("Creating CTk window...")
root = ctk.CTk()
root.title("Test Window")
root.geometry("400x300")

# Make it popup
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))

label = ctk.CTkLabel(root, text="👁️ If you can see this, CTk works!", font=("Arial", 20))
label.pack(pady=100)

print("Window created, starting mainloop...")
root.mainloop()
print("Window closed")
