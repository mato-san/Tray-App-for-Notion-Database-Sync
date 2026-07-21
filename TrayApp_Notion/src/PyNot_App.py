import subprocess
import sys
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

sync_process = None
print("Current working directory:", os.getcwd())
print("Script directory:", os.path.dirname(os.path.abspath(__file__)))


def run_sync(icon, item):
    global sync_process

    if sync_process is None or sync_process.poll() is not None:

        exe = os.path.join(
            os.path.dirname(sys.executable),
            "Notion_Python.exe"
        )

        print(exe)

        sync_process = subprocess.Popen([exe])
        print("Launching:", exe)
        print("Exists:", os.path.exists(exe))


icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
icon_image = Image.open(icon_path)

def quit(icon):
    global running
    running = False
    icon.stop()

icon = Icon(
    "My App",
    icon_image,
    menu=Menu(
        MenuItem("Run Database Sync", run_sync),
        MenuItem("Quit", quit)
    )
)

icon.run()