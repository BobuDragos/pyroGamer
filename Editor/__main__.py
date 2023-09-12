


import sys
import typing
import argparse
import json
import subprocess
import os
import configparser
import pprint
import textwrap
import ast
from pathlib import Path
from colorama import Fore, Back, Style, init
init(autoreset=True)
print(Fore.BLACK + Style.BRIGHT + "start pyroGamer.Editor...")

from PyQt6 import QtCore

from PyQt6.QtCore import (
    QSize, Qt,
    QSortFilterProxyModel,
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QWidget, QTabWidget, 
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit,
    QGridLayout, QHBoxLayout, QVBoxLayout,
    QStatusBar,
)

from pyroGamer.Editor.Tabs import (
    HierarchyTab, AssetsTab, CanvasTab,
)

class ActiveProject:
    path = Path()
    ActiveSceneID = None

    def OpenProject(path):
        ActiveProject.path = Path(path).as_posix()


parser = argparse.ArgumentParser(description="Opening Editor")
parser.add_argument('-p', '--projectPath', help="Specify the project path")

args = parser.parse_args()

if(args.projectPath):
    ActiveProject.OpenProject(Path(args.projectPath))
    print(Fore.GREEN + "Received projectPath: " + ActiveProject.path)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        def GetWindowSize():
            result = subprocess.run(['python', '-m', 'pyroGamer.EditorConfig', '--GetWindowSize'],
                                    capture_output=True, text=True)
            if(result.returncode != 0):
                print(Fore.LIGHTBLACK_EX + textwrap.indent(pprint.pformat(result.stdout), '>'))
                print(Fore.RED + "Error: " + result.stderr)
                sys.exit(1)
            for line in result.stdout.splitlines():
                if(line.startswith("EditorWindowSize:")):
                    windowSize = line.replace("EditorWindowSize: ", "")
                    windowSize = ast.literal_eval(windowSize)
                    print(Fore.GREEN + "Received EditorWindowSize: " +
                          str(windowSize[0]) + "x" + str(windowSize[1]))
                    return QSize(windowSize[0], windowSize[1])
            
        self.setFixedSize(GetWindowSize())
        self.setWindowTitle("Editor")


        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()

        fileMenu = menu.addMenu("&File")
        fileMenu.addAction("&New Scene")
        fileMenu.addAction("&Open Scene...")
        fileMenu.addSeparator()
        fileMenu.addAction("&Save Scene")
        fileMenu.addAction("&Save Scene As...")
        fileMenu.addSeparator()
        fileMenu.addAction("&New Project...")
        fileMenu.addAction("&Open Project...")
        fileMenu.addSeparator()
        fileMenu.addAction("&Build Settings...")
        fileMenu.addAction("&Run")

        editMenu = menu.addMenu("&Edit")
        editMenu.addAction("&Undo")
        editMenu.addAction("&Redo")
        editMenu.addSeparator()
        editMenu.addAction("&Cut")
        editMenu.addAction("&Copy")
        editMenu.addAction("&Paste")
        editMenu.addSeparator()
        editMenu.addAction("&Delete")
        editMenu.addAction("&Duplicate")
        editMenu.addSeparator()
        editMenu.addAction("&Select All")
        editMenu.addAction("&Deselect All")

        assetsMenu = menu.addMenu("&Assets")
        createAssetsMenu = assetsMenu.addMenu("&Create")
        createAssetsMenu.addAction("&Folder")
        createAssetsMenu.addAction("&Python Script")
        createAssetsMenu.addAction("&Scene")
        createAssetsMenu.addAction("&Sprite")
        createAssetsMenu.addAction("&Audio Clip")
        createAssetsMenu.addAction("&Font")
        createAssetsMenu.addAction("&JSON")
        createAssetsMenu.addAction("&Sprite")
        createAssetsMenu.addAction("&3D Model")
        assetsMenu.addSeparator()
        assetsMenu.addAction("&Reveal in File Explorer")
        
        gameObjectMenu = menu.addMenu("&GameObject")
        gameObjectMenu.addAction("&Create Empty")
        gameObjectMenu.addAction("&Create Empty Child")
        gameObjectMenu.addSeparator()
        create3DMenu = gameObjectMenu.addMenu("&3D Objects")
        create3DMenu.addAction("&Cube")
        create3DMenu.addAction("&Sphere")
        create3DMenu.addAction("&Capsule")
        create3DMenu.addAction("&Cylinder")
        create3DMenu.addAction("&Plane")
        create3DMenu.addSeparator()
        create3DMenu.addAction("&Torus")
        create3DMenu.addAction("&Cone")
        create3DMenu.addAction("&Pyramid")
        create3DMenu.addAction("&Tube")
        create3DMenu.addAction("&Monkey")
        create3DMenu.addAction("&Donut")
        create3DMenu.addSeparator()
        create3DMenu.addAction("&3D Model")
        create2DMenu = gameObjectMenu.addMenu("&2D Objects")
        create2DMenu.addAction("&Text")
        create2DMenu.addAction("&Sprite")
        gameObjectMenu.addSeparator()
        gameObjectMenu.addAction("&Light")
        gameObjectMenu.addAction("&Camera")
        gameObjectMenu.addSeparator()
        gameObjectMenu.addAction("&Audio Source")
        gameObjectMenu.addAction("&Audio Listener")
        gameObjectMenu.addSeparator()

        componentMenu = menu.addMenu("&Component")
        meshMenu = componentMenu.addMenu("&Mesh")
        meshMenu.addAction("&Mesh Filter")
        meshMenu.addAction("&Mesh Renderer")
        physicsMenu = componentMenu.addMenu("&Physics")
        physicsMenu.addAction("&Rigidbody")
        physicsMenu.addSeparator()
        physicsMenu.addAction("&Box Collider")
        physicsMenu.addAction("&Sphere Collider")
        physicsMenu.addAction("&Capsule Collider")
        physicsMenu.addAction("&Mesh Collider")
        audioMenu = componentMenu.addMenu("&Audio")
        audioMenu.addAction("&Audio Source")
        audioMenu.addAction("&Audio Listener")
        renderingMenu = componentMenu.addMenu("&Rendering")
        renderingMenu.addAction("&Camera")
        renderingMenu.addAction("&Light")
        renderingMenu.addSeparator()
        renderingMenu.addAction("&Skybox")

        
        

        viewMenu = menu.addMenu("&View")
        viewMenu.addAction("&Scene View")
        viewMenu.addAction("&Game View")
        viewMenu.addAction("&Inspector")
        viewMenu.addAction("&Hierarchy")
        viewMenu.addAction("&Assets")
        viewMenu.addAction("&Console")
        viewMenu.addAction("&Project Settings")

        helpMenu = menu.addMenu("&Help")
        helpMenu.addAction("&About pyroGamer")
        helpMenu.addAction("&Manual")
        helpMenu.addSeparator()
        helpMenu.addAction("&Support")
        helpMenu.addAction("&Check for Updates")





        mainLayout = QHBoxLayout()

        leftLayout = QHBoxLayout()
        
        HierarchyTab_Widget = QTabWidget()
        HierarchyTab_Widget.setFixedSize(QSize(200, 800))
        HierarchyTab_Widget.addTab(HierarchyTab(), "Hierarchy")
        leftLayout.addWidget(HierarchyTab_Widget)

        AssetsTab_Widget = QTabWidget()
        AssetsTab_Widget.setFixedSize(QSize(200, 800))
        AssetsTab_Widget.addTab(AssetsTab(ActiveProject.path), "Assets")
        leftLayout.addWidget(AssetsTab_Widget)

        mainLayout.addLayout(leftLayout)

        middleLayout = QVBoxLayout()

        SceneTab_Widget = QTabWidget()
        SceneTab_Widget.setFixedSize(QSize(900, 600))
        SceneTab_Widget.addTab(CanvasTab(), "Scene View")
        middleLayout.addWidget(SceneTab_Widget)

        TerminalTab_Widget = QTabWidget()
        TerminalTab_Widget.setFixedSize(QSize(900, 200))
        TerminalTab_Widget.addTab(QWidget(), "Terminal")
        middleLayout.addWidget(TerminalTab_Widget)

        mainLayout.addLayout(middleLayout)

        rightLayout = QHBoxLayout()

        InspectorTab_Widget = QTabWidget()
        InspectorTab_Widget.setFixedSize(QSize(200, 800))
        InspectorTab_Widget.addTab(QWidget(), "Inspector")
        rightLayout.addWidget(InspectorTab_Widget)

        mainLayout.addLayout(rightLayout)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)



app = QApplication(sys.argv)

window = GUI()
window.show()

app.exec()