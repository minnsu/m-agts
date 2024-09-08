import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from .create_edit_chat_window import CreateEditChat
from .load_chat_window import LoadChat

from llms import hello

form_main_class = uic.loadUiType("gui/ui/main.ui")[0]
class Main(QMainWindow, form_main_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.center()

        self.btn_create_edit_chat.clicked.connect(self._btn_create_edit_chat)
        self.btn_load_chat.clicked.connect(self._btn_load_chat)
        self.btn_exit.clicked.connect(self._btn_exit)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def _btn_create_edit_chat(self):
        self.hide()
        self.create_edit_chat = CreateEditChat()
        self.create_edit_chat.exec()
        self.show()
    
    def _btn_load_chat(self):
        self.hide()
        self.load_chat = LoadChat()
        self.load_chat.exec()
        self.show()
    
    def _btn_exit(self):
        exit()
    