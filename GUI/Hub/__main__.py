import sys

from PyQt6.QtCore import (
    QSize, Qt,
    QSortFilterProxyModel,
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QWidget, QTabWidget, 
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit,
    QGridLayout, QVBoxLayout, QHBoxLayout,
)

from pyroGamer.GUI.Hub.Elements.Tabs import LocalTab

import pprint
import textwrap
import json
import subprocess
import argparse
from colorama import Fore, Back, Style, init
init(autoreset=True)

print(Fore.BLACK + Style.BRIGHT + "starting pyroGamer.Hub...")

parser = argparse.ArgumentParser(description='Hub Utility')
parser.add_argument('-v', '--verbose', action="store_true", help='Print more information')

subparsers = parser.add_subparsers(title= 'subcommands', dest='command')

setWindowSize_parser = subparsers.add_parser('SetWindowSize', help='Open on a specific window size')
setWindowSize_parser.add_argument('--width', required=True, type=int, help='Set Hub window width')
setWindowSize_parser.add_argument('--height', required=True,  type=int, help='Set Hub window height')



args = parser.parse_args()

WindowSize = None

if args.command == "SetWindowSize":
    print(Fore.BLUE + "Received Hub window size from cli")
    print(Fore.GREEN + "Setting Hub window size to " + str(args.width) + "x" + str(args.height))
    WindowSize = QSize(args.width, args.height)
    
else:
    print(Fore.BLUE + "No Hub window size received from cli")
    print(Fore.YELLOW + "Instantiating " + "pyroGamer.GUI.Hub.Configs" + " to get Hub window size...")
    result = subprocess.run(['python', '-m', 'pyroGamer.GUI.Hub.Configs', '--GetWindowSize'], capture_output=True, text=True)

    if args.verbose:
        print(Fore.LIGHTBLACK_EX + textwrap.indent(pprint.pformat(result.stdout), '>'))

    if result.returncode != 0:
        print(Fore.RED + Style.BRIGHT + "Error: " + str(result.stderr))
        sys.exit(1)

    for line in result.stdout.splitlines():
        if line.startswith("HubWindowSize:"):
            windowSize_data = line.replace("HubWindowSize: ", "")
            windowSize_data = json.loads(windowSize_data)

            WindowSize = QSize()
            WindowSize.setWidth(int(windowSize_data["WIDTH"]))
            WindowSize.setHeight(int(windowSize_data["HEIGHT"]))

            print(Fore.GREEN + "Received HubWindowSize: " + 
                  str(WindowSize.width()) + "x" + 
                  str(WindowSize.height()))





class HubWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Hub")

        self.setFixedSize(WindowSize)

        layout = QVBoxLayout()

        Tabs_Widget = QTabWidget()

        Tabs_Widget.addTab(LocalTab(), "Local Projects")
        # Tabs_Widget.addTab(Cloud(), "Cloud Projects")
        Tabs_Widget.tabBar().setMovable(True)

        layout.addWidget(Tabs_Widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = HubWindow()
window.show()

app.exec()
