from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QMainWindow, QPushButton, QApplication, QFileDialog)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import equalizer as eq
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import os

class window(QMainWindow):
    pathIn = None
    pathTo = None
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(80,20,1080,720)
        self.setWindowTitle('Histogram Equalizer')
        self.setWindowIcon(QIcon('graph.ico'))

        actionQuit = QAction('&Leave', self)
        actionQuit.setShortcut('Ctrl+Q')
        actionQuit.setStatusTip('Leaving the app')
        actionQuit.triggered.connect(self.close_app)

        actionChooseIn = QAction("Choose the input image", self)
        actionChooseIn.setShortcut('Ctrl+I')
        actionChooseIn.triggered.connect(self.choose_input_image)
        
        actionChooseTo = QAction("Choose the target image", self)
        actionChooseTo.setShortcut('Ctrl+T')
        actionChooseTo.triggered.connect(self.choose_target_image)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(actionQuit)
        fileMenu.addAction(actionChooseIn)
        fileMenu.addAction(actionChooseTo)

        actionEqualize = QAction('Equalize Histogram', self)
        actionEqualize.triggered.connect(self.equalize_hist)

        self.toolBar = self.addToolBar('Extraction')
        self.toolBar.addAction(actionEqualize)

        self.mainW()

    def mainW(self):
        btn = QPushButton('EXIT', self)
        btn.clicked.connect(self.close_app)
        btn.setToolTip('Click to <b>EXIT</b>')
        btn.resize(btn.sizeHint())
        btn.move(594,20)

        self.show()

    def close_app(self):
        print('caution!!!')
        sys.exit()


    def choose_input_image(self):
        imIn = QLabel(self)
        image = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.pathIn = image[0]
        pixmapI = QPixmap(self.pathIn)
        imIn.setPixmap(pixmapI)
        imIn.resize(pixmapI.width(),pixmapI.height())
        imIn.move(20,60)
        self.show()
        imIn.show()
    
    def choose_target_image(self):
        imTo = QLabel(self)
        image = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.pathTo = image[0]
        pixmapT = QPixmap(self.pathTo)
        imTo.setPixmap(pixmapT)
        imTo.resize(pixmapT.width(),pixmapT.height())
        imTo.move(307,60)
        self.show()
        imTo.show()

    def equalize_hist(self):
        imIn = cv2.imread(self.pathIn)
        imTo = cv2.imread(self.pathTo)

        hist_In = eq.create_hist(imIn)
        hist_To = eq.create_hist(imTo)

        pdf_In = eq.pdf_create(hist_In)
        pdf_To = eq.pdf_create(hist_To)

        cdf_In = eq.cdf_create(pdf_In)
        cdf_To = eq.cdf_create(pdf_To)

        LUT = eq.generate_LUT(cdf_In, cdf_To)
        image = eq.remapper(imIn,LUT)
        cv2.imwrite("__save_temp__.png", image)

        imgQ = QLabel(self)
        pixmapQ = QPixmap("./__save_temp__.png")
        imgQ.setPixmap(pixmapQ)
        imgQ.resize(pixmapQ.width(),pixmapQ.height())
        imgQ.move(594,60)
        self.show()
        imgQ.show()

        if os.path.exists("./__save_temp__.png"):
            os.remove("./__save_temp__.png")
        else:
            pass

def run():
    app = QApplication(sys.argv)
    gui_ = window()
    sys.exit(app.exec_())

run()