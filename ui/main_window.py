import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import config
import pyperclip
from core.capture import ScreenCapture
from core.config_manager import ConfigManager
from core.live_translator import LiveTranslator
from core.ocr import OCREngine
from core.tray import TrayIcon
from core.translator import Translator
from ui.indicator import SelectionIndicator
from ui.popup_window import PopupWindow
from ui.settings_window import SettingsWindow
from ui.toolbar import Toolbar


class MainWindow:
    def __init__(self, root, config_manager=None):
        self.root = root
        self.config_manager = config_manager or ConfigManager()
        self.capture = ScreenCapture()
        self.ocr = OCREngine(tesseract_path=config.TESSERACT_PATH)
        self.translator = None
        self.live_translator = None
        self.popup = None
        self.indicator = None
        self.history = []

        self.setup_ui()
        self.setup_tray()
        self.setup_toolbar()
        self.refresh_translator()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        bg_color = "#f0f2f5"
        accent_color = "#4a90e2"
        text_color = "#333333"
        white = "#ffffff"

        self.root.configure(bg=bg_color)

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), background=bg_color, foreground=text_color)
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), background=bg_color, foreground="#555555")
        style.configure("TButton", font=("Segoe UI", 10), padding=6, borderwidth=0, background="#e1e4e8")
        style.map("TButton", background=[("active", "#d1d4d8")])
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), background=accent_color, foreground=white)
        style.map("Action.TButton", background=[("active", "#357abd")])

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Screen Translator", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        self.capture_btn = ttk.Button(
            main_frame,
            text="画面を選択して翻訳 (Ctrl+T)",
            command=self.on_capture_button_click,
            style="Action.TButton",
            cursor="hand2",
        )
        self.capture_btn.pack(fill=tk.X, pady=(0, 20), ipady=8)

        ttk.Label(main_frame, text="原文", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.original_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            font=("Segoe UI", 10),
            bg=white,
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.original_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        ttk.Label(main_frame, text="翻訳結果", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.translated_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            font=("Segoe UI", 10),
            bg=white,
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.translated_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))

        self.copy_btn = ttk.Button(action_frame, text="コピー", command=self.copy_to_clipboard)
        self.copy_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.history_btn = ttk.Button(action_frame, text="履歴", command=self.show_history)
        self.history_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.settings_btn = ttk.Button(action_frame, text="設定", command=self.open_settings)
        self.settings_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(20, 0))

        self.status_var = tk.StringVar(value="準備完了 (Ctrl+T でキャプチャ)")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.FLAT,
            anchor=tk.W,
            padding=(10, 5),
            background="#e0e0e0",
            font=("Segoe UI", 9),
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.bind("<Control-t>", lambda event: self.on_capture_button_click())

    def refresh_translator(self):
        api_key = self.config_manager.get_api_key()
        if not api_key:
            self.translator = None
            return

        try:
            self.translator = Translator(api_key=api_key)
        except ValueError:
            self.translator = None

    def copy_to_clipboard(self):
        text = self.translated_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.update_status("翻訳結果をコピーしました")
        else:
            self.update_status("コピーするテキストがありません")

    def on_capture_button_click(self):
        if not self.translator:
            messagebox.showerror(
                "API キー未設定",
                "OpenAI API キーが設定されていません。\n"
                "環境変数 OPENAI_API_KEY または設定画面から入力してください。\n\n"
                f"設定保存先:\n{self.config_manager.settings_path}",
                parent=self.root,
            )
            return

        self.root.iconify()
        self.root.after(200, self._start_capture)

    def _start_capture(self):
        result = self.capture.capture_region()

        try:
            self.root.deiconify()
            self.toolbar.show()
        except Exception:
            pass

        if result is None or result[0] is None:
            self.update_status("キャプチャをキャンセルしました")
            return

        image, _coords = result

        def start_processing():
            self.status_var.set("処理中...")
            self.capture_btn.config(state=tk.DISABLED)
            self.progress.start(10)
            threading.Thread(target=self._process_image, args=(image,), daemon=True).start()

        self.root.after(0, start_processing)

    def _process_image(self, image):
        try:
            self.update_status("文字認識中...")
            text = self.ocr.extract_text(image, lang="jpn+eng")

            if not text:
                self.show_error("テキストが検出されませんでした。")
                return

            self.root.after(0, lambda: self.show_original(text))
            self.update_status("翻訳中...")

            result = self.translator.translate(
                text,
                source_lang=self.config_manager.get("source_lang"),
                target_lang=self.config_manager.get("target_lang"),
            )

            if result["success"]:
                translated = result["translated"]
                self.root.after(0, lambda: self.show_translation(translated))
                self.update_status("完了")
                self.history.insert(0, {"original": text, "translated": translated})
                if len(self.history) > 5:
                    self.history.pop()

                if self.config_manager.get("auto_copy"):
                    self.root.after(0, lambda: pyperclip.copy(translated))
            else:
                self.show_error(result["error"])
        except Exception as exc:
            self.show_error(f"予期しないエラー: {exc}")
        finally:
            self.root.after(0, lambda: self.capture_btn.config(state=tk.NORMAL))
            self.root.after(0, self.progress.stop)

    def show_original(self, text):
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(tk.END, text)

    def show_translation(self, text):
        self.translated_text.delete(1.0, tk.END)
        self.translated_text.insert(tk.END, text)

    def show_error(self, message):
        self.root.after(0, lambda: messagebox.showerror("エラー", message, parent=self.root))
        self.update_status("エラーが発生しました")

    def update_status(self, message):
        self.root.after(0, lambda: self.status_var.set(message))

    def open_settings(self):
        was_withdrawn = self.root.state() == "withdrawn"
        if was_withdrawn:
            self.root.deiconify()
            self.root.update_idletasks()

        SettingsWindow(self.root, self.config_manager, on_save=self.on_settings_saved)

        if was_withdrawn:
            self.root.withdraw()

    def on_settings_saved(self):
        self.refresh_translator()
        self.update_status(f"設定を保存しました: {self.config_manager.settings_path}")

    def show_history(self):
        if not self.history:
            messagebox.showinfo("履歴", "履歴はまだありません。", parent=self.root)
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("履歴 (最新 5 件)")
        history_window.geometry("420x300")

        listbox = tk.Listbox(history_window)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for item in self.history:
            summary = item["original"][:30].replace("\n", " ")
            if len(item["original"]) > 30:
                summary += "..."
            listbox.insert(tk.END, summary)

        def load_selected(_event):
            selection = listbox.curselection()
            if selection:
                item = self.history[selection[0]]
                self.show_original(item["original"])
                self.show_translation(item["translated"])
                history_window.destroy()

        listbox.bind("<Double-1>", load_selected)

    def setup_tray(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.png")
        self.tray = TrayIcon(
            icon_path=icon_path,
            on_capture=self.on_tray_capture,
            on_show=self.on_tray_show,
            on_quit=self.on_tray_quit,
        )
        self.tray.run()

    def setup_toolbar(self):
        self.toolbar = Toolbar(
            self.root,
            on_capture=self.on_toolbar_capture,
            on_live=self.on_toolbar_live,
            on_home=self.on_toolbar_home,
        )

    def on_toolbar_home(self):
        self.root.deiconify()
        self.root.lift()

    def on_toolbar_capture(self):
        self.root.after(0, self.on_capture_button_click)

    def on_toolbar_live(self):
        self.refresh_translator()
        if not self.translator:
            self.toolbar.show()
            messagebox.showerror(
                "API キー未設定",
                "ライブ翻訳を使うには OpenAI API キーの設定が必要です。",
                parent=self.root,
            )
            return

        self.root.iconify()
        self.root.after(200, self._start_live_capture)

    def _start_live_capture(self):
        result = self.capture.capture_region()

        if result is None or result[0] is None:
            self.toolbar.show()
            return

        _image, coords = result
        self.start_live_translation(coords)
        self.show_indicator(coords)
        self.show_popup()

    def start_live_translation(self, coords):
        if self.live_translator:
            self.live_translator.stop()

        self.refresh_translator()
        if not self.translator:
            self.toolbar.show()
            return

        self.live_translator = LiveTranslator(
            capture_coords=coords,
            ocr_engine=self.ocr,
            translator=self.translator,
            on_update=self.on_live_update,
            on_error=self.on_live_error,
        )
        self.live_translator.source_lang = self.config_manager.get("source_lang")
        self.live_translator.target_lang = self.config_manager.get("target_lang")
        self.live_translator.start()

    def show_indicator(self, coords):
        if self.indicator:
            self.indicator.close()
        self.indicator = SelectionIndicator(self.root, coords)

    def show_popup(self):
        if self.popup:
            self.popup.close()
        self.popup = PopupWindow(self.root, on_close=self.stop_live_translation)

    def stop_live_translation(self):
        if self.live_translator:
            self.live_translator.stop()
            self.live_translator = None

        if self.indicator:
            self.indicator.close()
            self.indicator = None

        self.popup = None
        self.toolbar.show()

    def on_live_update(self, text):
        if self.popup:
            self.root.after(0, lambda: self.popup.update_text(text))

    def on_live_error(self, error):
        if self.popup:
            self.root.after(0, lambda: self.popup.update_text(f"エラー: {error}"))

    def on_closing(self):
        self.root.withdraw()
        self.toolbar.show()

    def on_tray_capture(self):
        self.root.after(0, self.on_capture_button_click)

    def on_tray_show(self):
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.toolbar.show)

    def on_tray_quit(self):
        self.root.after(0, self._quit_app)

    def _quit_app(self):
        if self.live_translator:
            self.live_translator.stop()
        self.tray.stop()
        self.root.destroy()
