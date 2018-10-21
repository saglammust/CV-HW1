from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QMainWindow, QPushButton, QApplication, QMenu)
from PyQt5.QtWidgets import (QVBoxLayout, QGroupBox, QFileDialog, QMessageBox, QSizePolicy, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import equalizer as eq
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import os
import random

class PlotWidget(QWidget):
    def __init__(self, hist, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.setGeometry(0,0,400,420)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.plotHist(hist)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plotHist(self, hist):
        self.figure.clear()

        ax2 = self.figure.add_axes([0.15, 0.72, 0.82, 0.26])
        ax2.bar(range(256), hist[:,0,2], width=1, color = 'red')
        ax1 = self.figure.add_axes([0.15, 0.38, 0.82, 0.26])
        ax1.bar(range(256), hist[:,0,1], width=1, color = 'green')
        ax0 = self.figure.add_axes([0.15, 0.06, 0.82, 0.26])
        ax0.bar(range(256), hist[:,0,0], width=1, color = 'blue')
        self.canvas.draw()

class window(QMainWindow):
    img_input = None
    img_target = None
    inputLoad = False
    targetLoad = False

    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.setGeometry(30,30,1200,720)
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
        fileMenu.addAction(actionChooseIn)
        fileMenu.addAction(actionChooseTo)
        fileMenu.addAction(actionQuit)

        actionEqualize = QAction('Equalize Histogram', self)
        actionEqualize.triggered.connect(self.equalize_hist)

        self.toolBar = self.addToolBar('Toolbar')
        self.toolBar.addAction(actionEqualize)
        self.initUI()

    def initUI(self):
        self.gb_input = QGroupBox('Input',self)
        self.gb_input.setStyleSheet('border: 1px;'
                 'QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top left;'
                 'padding-left: 3px;'
                 'padding-right: 3px;'
                 'margin-left: 10px }')
        self.gb_input.resize(400,690)
        self.gb_input.move(40,50)

        self.gb_target = QGroupBox('Target',self)
        self.gb_target.setStyleSheet('border: 1px;'
                 'QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top left;'
                 'padding-left: 3px;'
                 'padding-right: 3px;'
                 'margin-left: 10px }')
        self.gb_target.resize(400,690)
        self.gb_target.move(470,50)

        self.gb_output = QGroupBox('Output',self)
        self.gb_output.setStyleSheet('border: 1px;'
                 'QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top left;'
                 'padding-left: 3px;'
                 'padding-right: 3px;'
                 'margin-left: 10px }')
        self.gb_output.resize(400,690)
        self.gb_output.move(900,50)
        
        self.show()

    def close_app(self):
        sys.exit()

    def choose_input_image(self):
        self.gb_input.clear()
        QPixmapCache.clear()
        imIn = QLabel(self)
        path = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.img_input = cv2.imread(path[0])
        self.inputLoad = True
        image = QImage(self.img_input, self.img_input.shape[1], self.img_input.shape[0], \
                self.img_input.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap(image)
        pix_scaled = pix.scaled(380,240, Qt.KeepAspectRatio)
        imIn.setPixmap(pix_scaled)
        imIn.resize(pix_scaled.width(),pix_scaled.height())
        imIn.move(50,70)

        hist_In = eq.create_hist(self.img_input)
        plotHistofInput = PlotWidget(hist_In, self)
        plotHistofInput.move(40,320)
        plotHistofInput.show()

        imIn.show()

    def choose_target_image(self):
        QPixmapCache.clear()
        imTo = QLabel(self)
        path = QFileDialog.getOpenFileName(None,'Open File', '', "Image files(*.png)")
        self.img_target = cv2.imread(path[0])
        self.targetLoad = True
        
        image = QImage(self.img_target, self.img_target.shape[1], self.img_target.shape[0], \
                self.img_target.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap(image)
        pix_scaled = pix.scaled(380,240, Qt.KeepAspectRatio)
        imTo.setPixmap(pix_scaled)
        imTo.resize(pix_scaled.width(),pix_scaled.height())
        imTo.move(480,70)

        hist_To = eq.create_hist(self.img_target)
        plotHistofTarget = PlotWidget(hist_To, self)
        plotHistofTarget.move(470,320)
        plotHistofTarget.show()
        
        imTo.show()

    def equalize_hist(self):
        QPixmapCache.clear()
        if not self.inputLoad or not self.targetLoad:
            mistake = QMessageBox.warning(self, 'Crucial Mistake', 'You have not loaded either of the images!\n'
                'Please load the images and try again!', QMessageBox.Ok)
            if mistake == QMessageBox.Ok:
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
        pix_scaled = pix.scaled(380,240, Qt.KeepAspectRatio)
        imgOut.setPixmap(pix_scaled)
        imgOut.resize(pix_scaled.width(),pix_scaled.height())
        imgOut.move(910,70)

        hist_Out = eq.create_hist(img_out)
        plotHistofOutput = PlotWidget(hist_Out, self)
        plotHistofOutput.move(900,320)
        plotHistofOutput.show()

        imgOut.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())