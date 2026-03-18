import tkinter as tk
import ctypes

class SelectionIndicator:
    def __init__(self, root, coords):
        self.root = root
        self.coords = coords
        
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.3) # Semi-transparent
        self.window.configure(bg="red")
        
        # Position exactly over the captured area
        x = int(coords['x'])
        y = int(coords['y'])
        w = int(coords['width'])
        h = int(coords['height'])
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        
        # Try to make it click-through (Windows only)
        try:
            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
            # GWL_EXSTYLE = -20
            # WS_EX_TRANSPARENT = 0x00000020
            # WS_EX_LAYERED = 0x00080000
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            style = style | 0x00000020 | 0x00080000
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
        except Exception as e:
            print(f"Could not set click-through style: {e}")

    def close(self):
        self.window.destroy()
