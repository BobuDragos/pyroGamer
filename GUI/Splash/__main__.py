
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





def splash_ended():

    splash.close()
    print("splash ended")
    # subprocess.run(["python", "-m", "pyroGamer.Hub"])
    sys.exit(0)




# splashImage = QPixmap('images/pyroTf2.jpg')
# splashImage = splashImage.scaled(QSize(250, 250), Qt.AspectRatioMode.KeepAspectRatio)

# splash = QSplashScreen(splashImage)
# splash.show()

# QTimer.singleShot(250, splash_ended)


class SplashScreen(QSplashScreen):
    def init(self):
        self.size = QSize(250,250)
        self.pixmap = QPixmap('pyroGamer/GUI/Splash/images/pyroTf2.jpg')
        self.pixmap = self.pixmap.scaled(self.size, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(self.pixmap)

        print("before splash call")
        self.show()
        # QSplashScreen(self.image).show()
        print("after splash call")

        self.close()




app = QApplication(sys.argv)

# splashImage = QPixmap('pyroGamer/GUI/Splash/images/pyroTf2.jpg')
# splashImage = splashImage.scaled(QSize(250, 250), Qt.AspectRatioMode.KeepAspectRatio)

splash = SplashScreen
# splash.show()

QTimer.singleShot(250, splash_ended)

app.exec()