import os
import sys
import unittest
from unittest.mock import patch

from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ocr import OCREngine


class TestOCREngine(unittest.TestCase):
    def setUp(self):
        self.ocr = OCREngine()

    @patch("core.ocr.pytesseract")
    def test_extract_text(self, mock_pytesseract):
        mock_pytesseract.image_to_string.return_value = "Detected Text"

        image = Image.new("RGB", (100, 100), color="white")
        text = self.ocr.extract_text(image)

        self.assertEqual(text, "Detected Text")
        mock_pytesseract.image_to_string.assert_called_once()

    @patch("core.ocr.pytesseract")
    def test_extract_text_empty(self, mock_pytesseract):
        mock_pytesseract.image_to_string.return_value = "   \n  "

        image = Image.new("RGB", (100, 100), color="white")
        text = self.ocr.extract_text(image)

        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
