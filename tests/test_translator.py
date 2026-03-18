import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.translator import Translator

class TestTranslator(unittest.TestCase):
    @patch('core.translator.OpenAI')
    def test_translate_success(self, mock_openai):
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create translator instance (will use mocked OpenAI)
        translator = Translator(api_key="test_api_key")
        
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "こんにちは"
        mock_client.chat.completions.create.return_value = mock_response

        # Test translation
        result = translator.translate("Hello", "English", "Japanese")
        
        # Verify result
        self.assertTrue(result["success"])
        self.assertEqual(result["translated"], "こんにちは")
        self.assertIsNone(result.get("error"))
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()

    @patch('core.translator.OpenAI')
    def test_translate_failure(self, mock_openai):
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Create translator instance
        translator = Translator(api_key="test_api_key")
        
        # Mock an exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Test translation failure
        result = translator.translate("Hello", "English", "Japanese")
        
        # Verify result
        self.assertFalse(result["success"])
        self.assertEqual(result["translated"], "")  # Should be empty string, not None
        self.assertIn("API Error", result["error"])

if __name__ == '__main__':
    unittest.main()
