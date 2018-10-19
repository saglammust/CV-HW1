from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QMainWindow, QPushButton, QApplication, QFileDialog, QMessageBox)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import equalizer as eq
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import os

class window(QMainWindow):
    img_input = None
    img_target = None
    inputLoad = False
    targetLoad = False
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(80,20,1280,720)
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
        path = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.img_input = cv2.imread(path[0])
        self.inputLoad = True
        
        image = QImage(self.img_input, self.img_input.shape[1], self.img_input.shape[0], \
                self.img_input.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap(image)
        pix_scaled = pix.scaled(240,480, Qt.KeepAspectRatio)
        imIn.setPixmap(pix_scaled)
        imIn.resize(pix_scaled.width(),pix_scaled.height())
        imIn.move(10,60)
        self.show()
        imIn.show()
    
    def choose_target_image(self):
        imTo = QLabel(self)
        path = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.img_target = cv2.imread(path[0])
        self.targetLoad = True
        
        image = QImage(self.img_target, self.img_target.shape[1], self.img_target.shape[0], \
                self.img_target.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap(image)
        pix_scaled = pix.scaled(240,480, Qt.KeepAspectRatio)
        imTo.setPixmap(pix_scaled)
        imTo.resize(pix_scaled.width(),pix_scaled.height())
        imTo.move(480,60)
        self.show()
        imTo.show()
        
    def equalize_hist(self):
        if not self.inputLoad or not self.targetLoad:
            mistake = QMessageBox.warning(self, 'Crucial Mistake', 'You have not loaded either of the images!\n'
                'Please load the images and try again!', QMessageBox.Cancel)
            if mistake == QMessageBox.Cancel:
                return

        hist_In = eq.create_hist(self.img_input)
        hist_To = eq.create_hist(self.img_target)

        pdf_In = eq.pdf_create(hist_In)
        pdf_To = eq.pdf_create(hist_To)

        cdf_In = eq.cdf_create(pdf_In)
        cdf_To = eq.cdf_create(pdf_To)

        LUT = eq.generate_LUT(cdf_In, cdf_To)
        img_out = eq.remapper(self.img_input,LUT)

        imgOut = QLabel(self)
        image = QImage(img_out, img_out.shape[1], img_out.shape[0], img_out.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap(image)
        pix_scaled = pix.scaled(240,480, Qt.KeepAspectRatio)
        imgOut.setPixmap(pix_scaled)
        imgOut.resize(pix_scaled.width(),pix_scaled.height())
        imgOut.move(950,60)
        self.show()
        imgOut.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window()
    sys.exit(app.exec_())
