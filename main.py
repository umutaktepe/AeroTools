import sys
from PyQt5 import QtWidgets, QtGui
from aerotools.ui.main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icons/planeicon.png'))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
