import sys
from PyQt5.QtWidgets import QApplication
from Mainwindow import Application

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())








