import datetime
import sys
import re
import random
import time
from datetime import datetime
import csv
import numpy as np
import math
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QVBoxLayout
from PyQt6.QtWidgets import QComboBox, QLabel
from PyQt6 import QtSerialPort, QtWidgets
from GWinstekUi import Ui_MainWindow

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import serial


def normalValue(value):
    try:
        pref = re.findall(r'\D', value)[0]
        if pref == ('k' or 'K'):
            pref = 1000
        elif pref == 'M':
            pref = 1000000
        else:
            pref = 1
    except:
        pref = 1

    freq = int(re.findall(r'\d+', value)[0]) * pref

    return freq


def reInOut(stroka):
    print(stroka)
    trueValueR = float(stroka[0:8]) * 10 ** float(stroka[9:12])
    lcdR = stroka[0:12]
    trueValueX = float(stroka[13:21]) * 10 ** float(stroka[22:25])
    lcdX = stroka[13:25]
    return trueValueR, trueValueX, lcdR, lcdX


def randomAnswer(command):
    command = command
    print(command)
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    randOut = [a, b]
    return randOut


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.modeExp = None
        self.freqStop, self.freqStart, self.freqPoints, self.freqSteps = None, None, None, None
        self.lineSteps, self.logSteps = None, None
        self.z1, self.z2 = None, None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.plotWidgetRX.setBackground('w')
        self.ui.plotWidgetPowRX.setBackground('w')
        self.ui.btnFetch.clicked.connect(self.fetch)
        self.ui.btnConnect.clicked.connect(self.meterConnect)
        self.ui.btnApply.clicked.connect(self.setupExpParam)
        self.ui.btnStart.clicked.connect(self.startExperiment)
        self.ui.btnPlot.clicked.connect(self.plotAE)
        self.ui.btnSave.clicked.connect(self.saveFile)
        self.ui.btnPlotModel.clicked.connect(self.plotModel)
        self.ui.btnClear.clicked.connect(self.plotClear)

        # self.show()


    # Не используем в этом варианте программы, режим всегда R-X
    """
    def setMode(self):
        if self.ui.radioButtonRX.isChecked():
            command = b'FUNC R-X'
            self.ser.write(command)
        elif self.ui.radioButtonCpD.isChecked():
            command = b'FUNC Cp-D'
            self.ser.write(command)
        elif self.ui.radioButtonCsD.isChecked():
            command = b'FUNC Cs-D'
            self.ser.write(command)

            # print(self.ser.readline())
    """
    def meterConnect(self):
        try:
            self.ser = serial.Serial('COM4',115200)
            command = b'FUNC R-X'
            self.ser.write(command)
        except:
            print(" Не подключен прибор, подключите/включите и перезапустите программу")

    def fetch(self):
        command = b'FETC?'
        self.ser.write(command)
        hotCommandAnswer = self.ser.readline()
        print(hotCommandAnswer)
        self.ui.lineHotCommandAns.setText(hotCommandAnswer)

    def freq(self):
        command = 'FREQ ' + str(self.freqStop)
        print(command)
        command = bytes(command, 'UTF-8')
        print(command)
        self.ser.write(command)

    def setupExpParam(self):
        try:
            self.freqStart = normalValue(self.ui.lineEditStartFreq.text())
            self.freqStop = normalValue(self.ui.lineEditStopFreq.text())
            self.freqPoints = normalValue(self.ui.lineEditPointsFreq.text())
            print(self.freqStart, self.freqStop, self.freqPoints)

            if self.ui.radioLine.isChecked():
                self.modeExp = True
                self.ui.labelChoosedMode.setText('Mode - Line')
            elif self.ui.radioLog.isChecked():
                self.modeExp = False
                self.ui.labelChoosedMode.setText('Mode - Log')
            else:
                self.modeExp = True
                self.ui.labelChoosedMode.setText('Mode - Line')

            self.ui.labelFreqStart.setText('Start - ' + str(self.freqStart) + 'Hz')
            self.ui.labelFreqStop.setText('Stop - ' + str(self.freqStop) + 'Hz')
            self.ui.labelFreqPoints.setText('Steps - ' + str(self.freqPoints))

            if self.modeExp:
                self.freqSteps = np.linspace(self.freqStart, self.freqStop, self.freqPoints)
                print(self.freqSteps)
                for freq in self.freqSteps:
                    print(freq)

            else:
                self.freqSteps = np.geomspace(self.freqStart, self.freqStop, self.freqPoints)
                print(self.freqSteps)
                for freq in self.freqSteps:
                    print(freq)

        except IndexError:
            print('Invalid parameters')

    def startExperiment(self):
        print(self.freqPoints, self.freqStart, self.freqStop, self.modeExp)
        if self.modeExp:
            self.expRX()
        else:
            self.expRX()

    def expRX(self):
        command = 'FREQ '
        self.expResultR = []
        self.expResultX = []
        for freq in self.freqSteps:
            freq = np.round(freq)
            TX = command + str(freq)
            TX = bytes(TX, 'UTF-8')
            self.ser.write(TX)
            time.sleep(1)
            self.ser.write(b'FETCH?')
            result = reInOut(self.ser.readline())
            self.expResultX.append(result[0])
            self.expResultR.append(result[1])
            print(result)
            print(result[0], ' ', result[1], ' ', freq)
        print(self.expResultX)
        print(self.expResultR)
    
    def plotClear(self):
        self.ui.plotWidgetRX.clear()
        self.ui.plotWidgetPowRX.clear()

    def plotAE(self):
        self.powerRX = np.sqrt((np.power(self.expResultR, 2) + np.power(self.expResultX, 2)))
        self.ui.plotWidgetRX.clear()
        self.ui.plotWidgetPowRX.clear()
        self.resultX = np.absolute(self.randResultX)
        self.ui.plotWidgetRX.plot(self.expResultR, self.resultX, symbol='o', symbolSize = 14, pen = 'w')
        self.ui.plotWidgetPowRX.plot(self.freqSteps, self.powerRX, symbol='o', symbolSize = 14, pen = 'w')

    def plotModel(self):
        r1 = int(self.ui.lineEditR1.text())
        r2 = int(self.ui.lineEditR2.text())
        c = float(self.ui.lineEditC.text())
        self.z1, self.z2 = [], []
        for step in self.freqSteps:
            w = 2*math.pi*step
            self.z1.append(r1 + (r2/(1+(w**2*c**2*r2**2))))
            self.z2.append((w*c*r2**2)/(1+(w**2*c**2*r2**2)))

        self.powZ = np.sqrt(np.power(self.z1, 2)+np.power(self.z2,2))
        self.ui.plotWidgetRX.plot(self.z1, self.z2, pen = 'black')
        self.ui.plotWidgetPowRX.plot(self.freqSteps, self.powZ, pen = 'black')

    def saveFile(self):
        today = datetime.now()
        path = 'results_' + str(today).replace('.','').replace(':','')
        with open(path, 'w') as f:
            writer = csv.writer(f)
            for index in range(0, len(self.z1)):
                row = [self.z1[index], self.z2[index]]
                writer.writerow(row)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()