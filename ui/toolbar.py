import tkinter as tk


class Toolbar:
    def __init__(self, root, on_capture, on_live, on_home):
        self.root = root
        self.on_capture = on_capture
        self.on_live = on_live
        self.on_home = on_home

        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", 0.8)

        self.bg_color = "#333333"
        self.hover_color = "#444444"
        self.window.configure(bg=self.bg_color)

        self.screen_width = self.window.winfo_screenwidth()
        self.collapsed_width = 110
        self.collapsed_height = 5
        self.expanded_width = 320
        self.expanded_height = 60
        self.is_expanded = False
        self.update_position(collapsed=True)

        self.frame = tk.Frame(self.window, bg=self.bg_color)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.capture_btn = tk.Button(
            self.frame,
            text="翻訳",
            command=self.on_capture_click,
            bg=self.bg_color,
            fg="white",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            activebackground=self.hover_color,
            activeforeground="white",
            cursor="hand2",
        )

        self.live_btn = tk.Button(
            self.frame,
            text="ライブ",
            command=self.on_live_click,
            bg=self.bg_color,
            fg="#ff6666",
            relief=tk.FLAT,
            font=("Segoe UI", 10, "bold"),
            activebackground=self.hover_color,
            activeforeground="#ff6666",
            cursor="hand2",
        )

        self.home_btn = tk.Button(
            self.frame,
            text="表示",
            command=self.on_home_click,
            bg=self.bg_color,
            fg="#cccccc",
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            activebackground=self.hover_color,
            activeforeground="white",
            cursor="hand2",
        )

        self.window.bind("<Enter>", self.expand)
        self.window.bind("<Leave>", self.collapse)

    def update_position(self, collapsed=True):
        width = self.collapsed_width if collapsed else self.expanded_width
        height = self.collapsed_height if collapsed else self.expanded_height
        x = (self.screen_width - width) // 2
        self.window.geometry(f"{width}x{height}+{x}+0")

    def expand(self, _event=None):
        if self.is_expanded:
            return
        self.is_expanded = True
        self.update_position(collapsed=False)
        self.window.attributes("-alpha", 1.0)
        self.capture_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.live_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.home_btn.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def collapse(self, _event=None):
        x, y = self.window.winfo_pointerxy()
        widget_x = self.window.winfo_rootx()
        widget_y = self.window.winfo_rooty()
        widget_w = self.window.winfo_width()
        widget_h = self.window.winfo_height()

        if (widget_x <= x <= widget_x + widget_w) and (widget_y <= y <= widget_y + widget_h):
            return

        if not self.is_expanded:
            return

        self.is_expanded = False
        self.update_position(collapsed=True)
        self.window.attributes("-alpha", 0.8)
        self.capture_btn.pack_forget()
        self.live_btn.pack_forget()
        self.home_btn.pack_forget()

    def on_capture_click(self):
        self.window.withdraw()
        if self.on_capture:
            self.on_capture()

    def on_live_click(self):
        self.window.withdraw()
        if self.on_live:
            self.on_live()

    def on_home_click(self):
        if self.on_home:
            self.on_home()

    def show(self):
        self.window.deiconify()
        self.update_position(collapsed=True)

    def hide(self):
        self.window.withdraw()
