from openai import OpenAI
import openai

class Translator:
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI APIキー
        """
        if not api_key:
            raise ValueError("API key is required")
        self.client = OpenAI(api_key=api_key)
    
    def translate(self, text: str, source_lang: str = "Japanese", 
                  target_lang: str = "English") -> dict:
        """
        テキストを翻訳
        
        Args:
            text: 翻訳するテキスト
            source_lang: ソース言語（例: "Japanese", "Chinese", "Korean"）
            target_lang: ターゲット言語（例: "English", "Japanese"）
        
        Returns:
            dict: {
                "success": bool,
                "original": str,
                "translated": str,
                "error": str (エラー時のみ)
            }
        """
        if not text or not text.strip():
            return {
                "success": False,
                "original": text,
                "translated": "",
                "error": "Text is empty"
            }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a translator. Translate from {source_lang} to {target_lang}. Return only the translation."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "original": text,
                "translated": translated_text
            }
            
        except openai.AuthenticationError:
            return {
                "success": False,
                "original": text,
                "translated": "",
                "error": "Authentication Error: Invalid API Key"
            }
        except openai.RateLimitError:
            return {
                "success": False,
                "original": text,
                "translated": "",
                "error": "Rate Limit Error: Too many requests"
            }
        except openai.APIConnectionError:
            return {
                "success": False,
                "original": text,
                "translated": "",
                "error": "Network Error: Could not connect to OpenAI"
            }
        except Exception as e:
            return {
                "success": False,
                "original": text,
                "translated": "",
                "error": f"Unexpected Error: {str(e)}"
            }
