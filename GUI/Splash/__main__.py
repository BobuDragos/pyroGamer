
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import QTimer, QSize, Qt


import subprocess
import sys
import json
import pprint

import textwrap
from termcolor import colored
from colorama import Fore, Back, Style, init
init(autoreset=True)


print(Fore.BLACK + Style.BRIGHT + "start splashScreen...")



# TODO: Add splash class for more complex splash screen with:
# - a loading message, loading bar, loading percentage, loading animation

if __name__ == "__main__":
    def splash_ended():
        splash.close()
        print("splash ended")
        subprocess.run(["python", "-m", "pyroGamer.GUI.Hub"])
        sys.exit(0)

    app = QApplication(sys.argv)

    splashImage = QPixmap('pyroGamer/GUI/Splash/images/pyroTf2.jpg')
    splashSize = QSize(250,250)
    splashImage = splashImage.scaled(splashSize, Qt.AspectRatioMode.KeepAspectRatio)

    splash = QSplashScreen(splashImage)
    splash.show()

    QTimer.singleShot(250, splash_ended)

    app.exec()