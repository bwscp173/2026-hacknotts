from gui.game import Game
import os
import platform

from gui.start_menu import StartMenu

if platform.system() == "Linux":
    if "DISPLAY" not in os.environ:
        os.environ["DISPLAY"] = ":0"
    import subprocess
    try:
        subprocess.run(["xhost", "+local:"])
    except Exception:
        pass

# game = Game(800, 600)
# game.run()

m = StartMenu(800, 600)
m.run()