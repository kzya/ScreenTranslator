from PIL import Image, ImageEnhance
import pytesseract
import os

class OCREngine:
    def __init__(self, tesseract_path: str = None):
        """
        Args:
            tesseract_path: Tesseract実行ファイルのパス
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_text(self, image: Image.Image, lang: str = "jpn+eng") -> str:
        """
        画像からテキストを抽出
        
        Args:
            image: PIL Image
            lang: Tesseract言語コード（例: "jpn+eng", "chi_sim", "kor"）
        
        Returns:
            str: 抽出されたテキスト
        """
        try:
            # 1. 画像を前処理
            processed_image = self.preprocess_image(image)
            
            # 2. pytesseract.image_to_string で認識
            # builder=0 (TextBuilder) is default
            text = pytesseract.image_to_string(processed_image, lang=lang)
            
            return text.strip()
        except pytesseract.TesseractNotFoundError:
            return "Error: Tesseract not found. Please install Tesseract OCR."
        except Exception as e:
            return f"Error during OCR: {str(e)}"
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        OCR精度向上のための前処理
        """
        # グレースケール化
        img = image.convert('L')
        
        # コントラスト調整（ImageEnhance使用）
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  # コントラストを2倍に
        
        # 必要に応じて二値化なども検討できるが、まずはシンプルに
        
        return img
