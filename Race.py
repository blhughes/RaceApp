# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets,uic
import enum
import sensor

class State(enum.Enum):
    READY = 1
    RACING = 2
    FINISHED = 3


class Ui(QtWidgets.QMainWindow):
    def reset(self):
        self.raceTimer = QtCore.QTime()
        self.state = State.READY
        self.lcd.display("0.00")

    def stop(self):
        if self.state is not State.RACING: return
        self.finishTimes.insert(0,self.raceTimer.elapsed()/1000.)
        self.finishTimes.pop()
        self.lcd.display("%0.2f"%self.finishTimes[0])
        self.state=State.FINISHED
        self.updateTable()

    def start(self):
        if self.state is not State.READY: return
        self.raceTimer.start()
        self.state = State.RACING

    def updateTable(self):
        for row,value in enumerate(self.finishTimes):
            self.table.setItem(0,row, QtWidgets.QTableWidgetItem("%0.2f"%value))

    def raceLoop(self):
        ch0 = self.sensor.read(0)
        ch1 = self.sensor.read(1)
        self.statusBar.showMessage("Ch0: %d \t Ch1: %d"%(ch0,ch1))
        if self.state is State.READY:
            self.label.setText("Ready")
            if self.sensor.trigger0():
                self.start()
        elif self.state is State.RACING:
            self.label.setText("Racing")
            self.lcd.display("%0.2f"%(self.raceTimer.elapsed()/1000.))
            if self.sensor.trigger1():
                self.stop()
        else: #State.FINISHED
            self.label.setText("Finished")
            


    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('RaceWindow.ui', self)

        self.statusBar = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        
        self.resetButton = self.findChild(QtWidgets.QPushButton, 'resetButton')
        
        self.startAction = self.findChild(QtWidgets.QAction, 'actionStart')
        self.stopAction = self.findChild(QtWidgets.QAction, 'actionStop')
        
        self.table = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.lcd = self.findChild(QtWidgets.QLCDNumber, 'lcdNumber')
        self.label = self.findChild(QtWidgets.QLabel, 'stateLabel')


        self.resetButton.clicked.connect(self.reset)
        self.stopAction.triggered.connect(self.stop)
        self.startAction.triggered.connect(self.start)

        
        self.sensor = sensor.Sensor()
        self.state = State.READY
        self.lcd.display("0.00")
        self.finishTimes = [0,0,0,0,0]


        self.raceTimer = QtCore.QTime()


        self.appTimer = QtCore.QTimer(self)
        self.appTimer.timeout.connect(self.raceLoop)
        self.appTimer.start(10)

        self.updateTable()
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())

