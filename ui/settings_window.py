import tkinter as tk
from tkinter import ttk


class SettingsWindow:
    def __init__(self, root, config_manager, on_save=None):
        self.root = root
        self.config_manager = config_manager
        self.on_save = on_save

        self.window = tk.Toplevel(root)
        self.window.title("設定")
        self.window.geometry("460x420")
        self.window.resizable(True, True)
        self.window.transient(root)
        self.window.grab_set()

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        padding = {"padx": 20, "pady": 10}

        lang_frame = ttk.LabelFrame(self.window, text="言語設定")
        lang_frame.pack(fill="x", **padding)

        ttk.Label(lang_frame, text="翻訳元").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_lang_var = tk.StringVar()
        self.source_lang_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang_var, state="readonly")
        self.source_lang_combo["values"] = ("English", "Japanese", "Chinese", "Korean", "French", "German", "Spanish")
        self.source_lang_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(lang_frame, text="翻訳先").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.target_lang_var = tk.StringVar()
        self.target_lang_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang_var, state="readonly")
        self.target_lang_combo["values"] = ("English", "Japanese", "Chinese", "Korean", "French", "German", "Spanish")
        self.target_lang_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        lang_frame.columnconfigure(1, weight=1)

        api_frame = ttk.LabelFrame(self.window, text="OpenAI API キー")
        api_frame.pack(fill="x", **padding)

        ttk.Label(api_frame, text="保存する API キー").pack(anchor="w", padx=5, pady=(5, 0))
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*")
        self.api_key_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(
            api_frame,
            text="環境変数 OPENAI_API_KEY が設定されている場合は、そちらが優先されます。",
            wraplength=400,
            foreground="gray",
        ).pack(anchor="w", padx=5, pady=(0, 5))

        path_frame = ttk.LabelFrame(self.window, text="設定保存先")
        path_frame.pack(fill="x", **padding)

        ttk.Label(
            path_frame,
            text=str(self.config_manager.settings_path),
            wraplength=400,
        ).pack(anchor="w", padx=5, pady=5)
        ttk.Label(
            path_frame,
            text="この設定ファイルは共有物に含めず、各ユーザーの PC にのみ保存されます。",
            wraplength=400,
            foreground="gray",
        ).pack(anchor="w", padx=5, pady=(0, 5))

        other_frame = ttk.LabelFrame(self.window, text="その他")
        other_frame.pack(fill="x", **padding)

        self.auto_copy_var = tk.BooleanVar()
        tk.Checkbutton(
            other_frame,
            text="翻訳結果を自動でコピーする",
            variable=self.auto_copy_var,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=5, pady=5)

        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", pady=20, padx=20)
        ttk.Button(button_frame, text="保存", command=self.save_settings).pack(side="right", padx=5)
        ttk.Button(button_frame, text="閉じる", command=self.window.destroy).pack(side="right", padx=5)

    def load_current_settings(self):
        self.source_lang_var.set(self.config_manager.get("source_lang"))
        self.target_lang_var.set(self.config_manager.get("target_lang"))
        self.api_key_var.set(self.config_manager.get("openai_api_key"))
        self.auto_copy_var.set(self.config_manager.get("auto_copy"))

    def save_settings(self):
        self.config_manager.set("source_lang", self.source_lang_var.get())
        self.config_manager.set("target_lang", self.target_lang_var.get())
        self.config_manager.set("openai_api_key", self.api_key_var.get().strip())
        self.config_manager.set("auto_copy", self.auto_copy_var.get())

        if self.on_save:
            self.on_save()

        self.window.destroy()
