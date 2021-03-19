import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5.QtWidgets import (
    QWidget, QApplication, QProgressBar, QMainWindow,
    QHBoxLayout, QPushButton
)

class Worker(QtCore.QObject):

    signalNumber = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Worker, self).__init__()
        self.i = 1
        self.stopped = False

    def doStuff(self):

        if not self.stopped:
            print("toggle to run")
        else:
            self.i += 1
            self.signalNumber.emit(self.i)

    def stop(self):
        self.stopped = not self.stopped
        print(f"toggled to {self.stopped}")

    def print_(self):
        print(self.i)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.worker = Worker()
        self.t = QtCore.QThread()
        self.worker.moveToThread(self.t)
        self.worker.signalNumber.connect(self.print)
        self.t.start()
        start_action = self.menuBar().addAction("Start", self.worker.doStuff)
        stop_action = self.menuBar().addAction("Stop", self.worker.stop)
        stop_quit = self.menuBar().addAction("Quit", self.quit_)

        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        
        self.btn_print = QPushButton("Print")
        self.btn_toggle = QPushButton("Toggle")
        self.btn_do = QPushButton("Do")
        
        l.addWidget(self.btn_print)
        l.addWidget(self.btn_toggle)
        l.addWidget(self.btn_do)
        
        self.setCentralWidget(w)

        self.btn_toggle.clicked.connect(self.worker.stop)
        self.btn_do.clicked.connect(self.worker.doStuff)
        self.btn_print.clicked.connect(self.worker.print_)

        self.show()

    def print(self, a0):
        print(a0)

    def quit_(self):
        while self.t.isRunning():
            print("quittng")
            self.t.quit()
        else:
            print("done!")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())