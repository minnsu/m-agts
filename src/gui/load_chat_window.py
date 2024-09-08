from PyQt5.QtWidgets import *
from PyQt5 import uic

form_create_edit_chat_class = uic.loadUiType("gui/ui/load_chat.ui")[0]
class LoadChat(QDialog, form_create_edit_chat_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_select_config.clicked.connect(self._btn_select_config)
        self.btn_stop.clicked.connect(self._btn_stop)
        self.btn_enter.clicked.connect(self._btn_enter)

    def _btn_select_config(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_config_path.setText(fname[0])
        
        # TODO: 파일을 읽어서 chating을 생성해야 함
        # + init_message가 존재하면 해당 값으로 설정할 것

    def _btn_stop(self):
        # TODO: chating 중지
        print("Error: Not Implemented [LoadChat._btn_stop]")
    
    def _btn_enter(self):
        # TODO: chating 시작 및 입력 메시지 전송
        print("Error: Not Implemented [LoadChat._btn_enter]")


    