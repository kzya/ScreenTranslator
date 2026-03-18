import os
import tkinter as tk
from tkinter import messagebox

import config
from core.config_manager import ConfigManager
from ui.main_window import MainWindow


def collect_startup_warnings(config_manager: ConfigManager):
    warnings = []

    if not os.path.exists(config.TESSERACT_PATH):
        warnings.append(
            "Tesseract OCR が見つかりません。\n"
            f"確認先:\n{config.TESSERACT_PATH}\n\n"
            "Tesseract をインストールするか、config.py のパスを見直してください。"
        )

    if not config_manager.get_api_key():
        warnings.append(
            "OpenAI API キーが未設定です。\n"
            "環境変数 OPENAI_API_KEY または設定画面から入力してください。\n\n"
            f"設定保存先:\n{config_manager.settings_path}"
        )

    return warnings


def main():
    config_manager = ConfigManager()

    root = tk.Tk()
    root.title("Screen Translator")
    root.geometry("600x700")
    root.resizable(False, False)

    MainWindow(root, config_manager=config_manager)

    for warning in collect_startup_warnings(config_manager):
        messagebox.showwarning("設定の確認", warning, parent=root)

    root.mainloop()


if __name__ == "__main__":
    main()
