import os
import sys

# OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Tesseract Path Detection
def get_tesseract_path():
    """
    Tesseractのパスを検出
    1. PyInstallerでビルドされた場合: 同梱されたTesseractを使用
    2. 開発環境: システムのTesseractを使用
    """
    if getattr(sys, 'frozen', False):
        # PyInstallerでビルドされた場合
        base_path = sys._MEIPASS
        tesseract_path = os.path.join(base_path, 'tesseract', 'tesseract.exe')
        if os.path.exists(tesseract_path):
            return tesseract_path
    
    # 開発環境またはフォールバック
    return r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TESSERACT_PATH = get_tesseract_path()

# Default Languages
DEFAULT_SOURCE_LANG = "English"
DEFAULT_TARGET_LANG = "Japanese"
