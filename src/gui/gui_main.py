import os
import sys

from PyQt5.QtWidgets import QApplication
from main_window import Main

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = Main() 

    myWindow.show()
    app.exec_()
