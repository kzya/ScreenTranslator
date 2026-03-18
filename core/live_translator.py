import threading
import time
from PIL import Image
import mss

class LiveTranslator:
    def __init__(self, capture_coords, ocr_engine, translator, on_update, on_error):
        self.coords = capture_coords
        self.ocr = ocr_engine
        self.translator = translator
        self.on_update = on_update
        self.on_error = on_error
        
        self.is_running = False
        self.thread = None
        self.last_text = ""
        self.interval = 2.0 # seconds
        
    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def _loop(self):
        with mss.mss() as sct:
            while self.is_running:
                try:
                    # Capture specific region
                    # mss requires monitor dict: {'top': y, 'left': x, 'width': w, 'height': h}
                    monitor = {
                        "top": int(self.coords["y"]),
                        "left": int(self.coords["x"]),
                        "width": int(self.coords["width"]),
                        "height": int(self.coords["height"])
                    }
                    
                    sct_img = sct.grab(monitor)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    
                    # OCR
                    text = self.ocr.extract_text(img, lang="jpn+eng")
                    
                    # Check for changes (simple string comparison)
                    # Ignore whitespace changes to reduce noise
                    clean_text = text.strip()
                    if clean_text and clean_text != self.last_text:
                        print(f"DEBUG: Text changed. New text: {clean_text[:20]}...")
                        self.last_text = clean_text
                        
                        # Translate
                        # Use instance variables for languages
                        result = self.translator.translate(
                            clean_text, 
                            source_lang=getattr(self, 'source_lang', 'English'), 
                            target_lang=getattr(self, 'target_lang', 'Japanese')
                        )
                        
                        if result["success"]:
                            self.on_update(result["translated"])
                        else:
                            self.on_error(result["error"])
                            
                except Exception as e:
                    print(f"Error in LiveTranslator: {e}")
                    self.on_error(str(e))
                    
                time.sleep(self.interval)
