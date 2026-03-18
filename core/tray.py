import threading
import pystray
from PIL import Image
import os

class TrayIcon:
    def __init__(self, icon_path, on_capture, on_show, on_quit):
        self.icon_path = icon_path
        self.on_capture = on_capture
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon = None
        self.thread = None

    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Capture", self.on_capture_clicked, default=True),
            pystray.MenuItem("Show Window", self.on_show_clicked),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.on_quit_clicked)
        )

    def on_capture_clicked(self, icon, item):
        if self.on_capture:
            self.on_capture()

    def on_show_clicked(self, icon, item):
        if self.on_show:
            self.on_show()

    def on_quit_clicked(self, icon, item):
        if self.on_quit:
            self.on_quit()

    def run(self):
        image = Image.open(self.icon_path)
        self.icon = pystray.Icon("ScreenTranslator", image, "Screen Translator", self.create_menu())
        
        # Run pystray in a separate thread to not block Tkinter
        self.thread = threading.Thread(target=self.icon.run, daemon=True)
        self.thread.start()

    def stop(self):
        if self.icon:
            self.icon.stop()
