
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


print(Fore.BLACK + Style.BRIGHT + "start pyroGamer...")

if __name__ == "__main__":
    # app = QApplication(sys.argv)

    subprocess.run(["python", "-m", "pyroGamer.GUI.Splash"])

    # app.exec()



