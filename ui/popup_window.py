import tkinter as tk
from tkinter import scrolledtext

import pyperclip


class PopupWindow:
    def __init__(self, root, on_close):
        self.root = root
        self.on_close = on_close

        self.window = tk.Toplevel(root)
        self.window.title("ライブ翻訳")
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.geometry("420x260+100+100")

        toolbar = tk.Frame(self.window, bg="#f0f0f0", height=30)
        toolbar.pack(fill="x", side="top")

        tk.Button(
            toolbar,
            text="コピー",
            command=self.copy_to_clipboard,
            relief="flat",
            bg="#f0f0f0",
        ).pack(side="left", padx=5, pady=2)

        self.text_area = scrolledtext.ScrolledText(
            self.window,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            padx=10,
            pady=10,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, "翻訳結果を待機中です...")
        self.text_area.configure(state="disabled")

    def update_text(self, text):
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state="disabled")

    def close(self):
        self.window.destroy()
        if self.on_close:
            self.on_close()

    def copy_to_clipboard(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            pyperclip.copy(text)
