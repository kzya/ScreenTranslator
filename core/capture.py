import tkinter as tk
from PIL import Image
import mss
import mss.tools

class ScreenCapture:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.rect = None
        self.overlay = None
        self.selection = None
        
    def capture_region(self) -> tuple[Image.Image, dict]:
        """
        画面キャプチャと領域選択を実行
        
        Returns:
            tuple: (選択領域の画像, 座標情報 {"x": int, "y": int, "width": int, "height": int})
            キャンセルされた場合は (None, None) を返す
        """
        # 1. mssで全画面キャプチャ
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # 全画面
            sct_img = sct.grab(monitor)
            # PIL Imageに変換
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
        self.full_screenshot = img
        self.selection = None
        
        # 2. Tkinterで全画面オーバーレイ表示
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)  # 半透明
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(background='black')
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # イベントバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.on_escape)
        
        # wait_windowを使用（mainloopの代わり）
        # これにより、このウィンドウが閉じられるまで待機するが、
        # メインウィンドウのイベントループはブロックしない
        self.root.wait_window(self.root)
        
        return self.selection
        
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # 既存の矩形があれば削除
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='white', width=2)

    def on_move_press(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        # current_x/yが設定されていない場合はeventから取得
        if self.current_x is None or self.current_y is None:
            self.current_x = event.x
            self.current_y = event.y
            
        # 座標の正規化（左上と右下を正しく判定）
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        width = x2 - x1
        height = y2 - y1
        
        print(f"Selection: ({x1}, {y1}) to ({x2}, {y2}), size: {width}x{height}")
        
        # 小さすぎる選択は無視（誤操作防止）
        if width < 10 or height < 10:
            print("Selection too small, ignoring")
            return

        # 選択領域を切り抜き
        cropped_img = self.full_screenshot.crop((x1, y1, x2, y2))
        
        self.selection = (cropped_img, {"x": x1, "y": y1, "width": width, "height": height})
        
        print("Selection successful, closing overlay")
        self.close_overlay()


    def on_escape(self, event):
        self.selection = (None, None)
        self.close_overlay()
        
    def close_overlay(self):
        self.root.destroy()
