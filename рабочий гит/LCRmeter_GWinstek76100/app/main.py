import sys
import re
import random
import time
import json
from datetime import datetime
import csv
import numpy as np
from numpy import median
import math
# , QWidget, QGraphicsScene, QVBoxLayout
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
# from PyQt6.QtWidgets import QComboBox, QLabel
# from PyQt6 import QtSerialPort, QtWidgets
from gui_v2.GWinstekUi import Ui_MainWindow
from gui_v2.GWinstekUi_plot import Ui_Form

# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg

import serial
# from app.lcrmeter.tools.auto_experiments.auto_experiments import autotest_each_freqs


def normalValue(value: str) -> int:
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


def reInOut(stroka: str):
    # print(stroka)
    trueValueR = float(stroka[0:8]) * 10 ** float(stroka[9:12])
    lcdR = stroka[0:12]
    trueValueX = float(stroka[13:21]) * 10 ** float(stroka[22:25])
    lcdX = stroka[13:25]
    return trueValueR, trueValueX, lcdR, lcdX


def randomAnswer(command: str):
    command = command
    print(command)
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    randOut = [a, b]
    return randOut



class SubWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.modeExp = None
        self.freqStop, self.freqStart, self.freqPoints, self.freqSteps = None, None, None, None
        self.level = None
        self.lineSteps, self.logSteps = None, None
        self.z1, self.z2 = None, None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.plotWidgetRX.setBackground('w')
        # self.ui.plotWidgetPowRX.setBackground('w')
        self.ui.btnFetch.clicked.connect(self.fetch)
        self.ui.btnConnect.clicked.connect(self.meterConnect)
        self.ui.btnApply.clicked.connect(self.setupExpParam)
        self.ui.btnStart.clicked.connect(self.startExperiment)
        self.ui.btnPlot.clicked.connect(self.plotAE)
        self.ui.btnSave.clicked.connect(self.saveFile)
        self.ui.btnPlotModel.clicked.connect(self.plotModelRandls)
        self.ui.btnClear.clicked.connect(self.plotClear)
        # self.ui.btnTest1.clicked.connect(self.autotest_each_freqs)

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
            self.ser = serial.Serial('COM4', 115200)
            command = b'FUNC R-X'
            self.ser.write(command)
        except:  # need add exception
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
            self.level = self.ui.lineEditPointsLevel.text()
            print(self.freqStart, self.freqStop, self.freqPoints, self.level)

            if self.ui.radioLine.isChecked():
                self.modeExp = True
                self.ui.labelChoosedMode.setText('Mode - Line')
            elif self.ui.radioLog.isChecked():
                self.modeExp = False
                self.ui.labelChoosedMode.setText('Mode - Log')
            else:
                self.modeExp = True
                self.ui.labelChoosedMode.setText('Mode - Line')

            self.ui.labelFreqStart.setText(
                'Start - ' + str(self.freqStart) + 'Hz')
            self.ui.labelFreqStop.setText(
                'Stop - ' + str(self.freqStop) + 'Hz')
            self.ui.labelFreqPoints.setText('Steps - ' + str(self.freqPoints))

            if self.modeExp:
                self.freqSteps = np.linspace(
                    self.freqStart, self.freqStop, self.freqPoints)
                print(self.freqSteps)
                for freq in self.freqSteps:
                    print(freq)

            else:
                self.freqSteps = np.geomspace(
                    self.freqStart, self.freqStop, self.freqPoints)
                print(self.freqSteps)
                for freq in self.freqSteps:
                    print(freq)

        except IndexError:
            print('Invalid parameters')

    def startExperiment(self):
        print(self.freqPoints, self.freqStart, self.freqStop, self.modeExp)

        points = self.freqPoints
        freq = self.freqStart
        stop = self.freqStop
        mode = self.modeExp
        level = self.level
        if mode:
            lineSteps = np.linspace(freq, stop, points)
            print(lineSteps)
            self.expRX(level, lineSteps)
        else:
            logSteps = np.geomspace(freq, stop, points)
            print(logSteps)
            self.expRX(level, logSteps)

    def expRX(self, level, freqSteps: list[float]):
        level_command = 'VOLT ' + str(level)
        txx = bytes(level_command, 'UTF-8')
        self.ser.write(txx)
        command = 'FREQ '
        self.expResultR = []
        self.expResultX = []

        self.freqSteps = []
        # l_freq = len(self.freqSteps)
        # pause_steps = []
        # for el in self.freqSteps:
        #     if el < 100:
        #         pause_steps.append(20)
        #     elif el < 100:
        #         pause_steps.append(10)
        #     else:
        #         pause_steps.append(2)

        # print(len(self.freqSteps), len(pause_steps))

        # for freq, pause in zip(freqSteps, pause_steps):
        for freq in freqSteps:
            # freq = np.round(freq)
            tx = command + str(freq)
            tx = bytes(tx, 'UTF-8')
            self.ser.write(tx)
            # pause = pause_steps[freqSteps.index(freq)]
            # pause = pause_steps[np.where(freqSteps==freq)[0][0]]
            if freq < 20:
                pause = 20
            elif freq < 100:
                pause = 10
            elif freq < 500:
                pause = 5
            else:
                pause = 0.3
            print(pause, freq)
            time.sleep(pause)
            tryResultX: list[float] = []
            tryResultR: list[float] = []
            Q = 5
            for tr in range(Q):

                time.sleep(0.10)
                self.ser.write(b'FETCH?')

                text = self.ser.readline()
                print(text)

                result = reInOut(text)
                tryResultX.append(result[1])
                tryResultR.append(result[0])

            # resX = sum(tryResultX)/Q
            # resR = sum(tryResultR)/Q
            resX = median(tryResultX)
            resR = median(tryResultR)
            print("###############")
            print("Findings of median")
            print(
                f"Median of R list - {tryResultR} = {resX}, of X list - {tryResultX} = {resX}")
            print("###############")

            # self.expResultX.append(result[1])
            # self.expResultR.append(result[0])

            self.expResultX.append(resX)
            self.expResultR.append(resR)
            self.freqSteps.append(freq)
            print(result)
            print(result[0], ' ', result[1], ' ', freq)
        print(self.expResultX)
        print(self.expResultR)

    def plotClear(self):
        self.ui.plotWidgetRX.clear()
        self.ui.plotWidgetPowRX.clear()

    def plotAE(self):
        self.powerRX = np.sqrt(
            (np.power(self.expResultR, 2) + np.power(self.expResultX, 2)))
        self.ui.plotWidgetRX.clear()
        self.ui.plotWidgetPowRX.clear()
        self.resultX = np.absolute(self.expResultX)
        # self.resultR = np.absolute(self.expResultR)
        self.ui.plotWidgetRX.plot(
            self.expResultR, self.resultX, symbol='o', symbolSize=14, pen='b')
        self.ui.plotWidgetPowRX.plot(
            self.freqSteps, self.powerRX, symbol='o', symbolSize=14, pen='b')
        print("######################")
        print(self.expResultR, self.resultX)
        print(self.freqSteps)
        print(self.powerRX)
        print("######################")

    def plotModelRandls(self):
        r1 = int(self.ui.lineEditModelRandR1.text())
        r2 = int(self.ui.lineEditModelRandR2.text())
        c = float(self.ui.lineEditModelRandC.text())
        self.z1, self.z2 = [], []

        mode = self.modeExp

        if mode:
            steps = np.linspace(self.freqStart, self.freqStop, self.freqPoints)
        else:
            steps = np.geomspace(
                self.freqStart, self.freqStop, self.freqPoints)

        for step in steps:
            w = 2 * math.pi * step
            self.z1.append(r1 + (r2/(1+((w**2)*(c**2)*(r2**2)))))
            self.z2.append((w*c*(r2**2))/(1+((w**2)*(c**2)*(r2**2))))

        self.powZ = np.sqrt(np.power(self.z1, 2)+np.power(self.z2, 2))
        self.ui.plotWidgetRX.plot(self.z1, self.z2, pen='black')
        self.ui.plotWidgetPowRX.plot(self.freqSteps, self.powZ, pen='black')
        print("######################")
        print(self.z1, self.z2)
        print(self.powZ)
        print("######################")

    def saveFile(self):
        today = datetime.now()
        path = f"results//results_{str(today).replace('.','').replace(':','')}{self.freqStart}Hz-{self.freqStop}Hz.csv"
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            for index in range(0, len(self.expResultX)):
                row = [self.freqSteps[index],
                       self.expResultR[index], self.expResultX[index]]
                print(row)
                writer.writerow(row)

    # def autotest_each_freqs(self):
    #     result_dict = {}
    #     freqs = [10, 100000, 50]
    #     level = 1
    #     logSteps = np.geomspace(freqs[0], freqs[1], freqs[2])
    #     for freq in logSteps:
    #         tryResultX: list[float] = []
    #         tryResultR: list[float] = []
    #         for step in range(2):
    #             command = 'FREQ '
    #             self.expResultR = []
    #             self.expResultX = []
    #             self.freqSteps = []

    #             tx = command + str(freq)
    #             tx = bytes(tx, 'UTF-8')
    #             self.ser.write(tx)

    #             time.sleep(0.5)

    #             self.ser.write(b'FETCH?')

    #             text = self.ser.readline()
    #             # print(text)

    #             result = reInOut(text)
    #             tryResultX.append(result[1])
    #             tryResultR.append(result[0])
    #         result_dict[f'{str(freq)}'] = {
    #             'X': tryResultX,
    #             'R': tryResultR,
    #         }

    #     with open('result.json', 'w') as fp:
    #         json.dump(result_dict, fp)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
