import json

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets

import autogen
from autogen import ConversableAgent, GroupChat, GroupChatManager

from llms import make_chat

class ChatWorker(QThread):
    def __init__(self, chat_objects, init_message):
        super().__init__()
        self.chat_objects = chat_objects
        self.init_message = init_message

    def run(self):
        initiator = self.chat_objects['initiator_agent']
        recipient = self.chat_objects['recipient']
        
        chat_result = initiator.initiate_chat(
            recipient,
            message=self.init_message,
            summary_method=self.chat_objects['summary_method'],
        )

form_create_edit_chat_class = uic.loadUiType("gui/ui/load_chat.ui")[0]
class LoadChat(QDialog, form_create_edit_chat_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_select_config.clicked.connect(self._btn_select_config)
        self.btn_stop.clicked.connect(self._btn_stop)
        self.btn_enter.clicked.connect(self._btn_enter)

        self.pte_user_input.keyPressEvent = self.keyPressEvent

        self.chat_config = None
        self.chat_objects = None
        self.chat_start_flag = False

        self.chat_worker = None

    def _btn_select_config(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_config_path.setText(fname[0])
        
        # TODO: 파일을 읽어서 chating을 생성해야 함
        # + init_message가 존재하면 해당 값으로 설정할 것

        print(fname[0])
        with open(fname[0], 'r') as f:
            self.chat_config = json.load(f)
            print(self.chat_config)

        self.chat_objects = make_chat(self.chat_config, self.message_callback)
        self.pte_user_input.setPlainText(self.chat_objects['init_message'])

    def _btn_stop(self):
        if self.chat_worker:
            self.tb_chat.append(
                'Chatting stopped.\n'
            )
            self.chat_worker.terminate()
            self.chat_worker = None
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() == Qt.ShiftModifier: # Shift + Enter
                pass
            else:
                self._btn_enter()
        QtWidgets.QPlainTextEdit.keyPressEvent(self.pte_user_input, event)

    def _btn_enter(self):
        init_message = self.pte_user_input.toPlainText()
        self.pte_user_input.clear()

        if self.chat_start_flag == False:
            self.chat_start_flag = True
            self.chat_worker = ChatWorker(self.chat_objects, init_message)
            self.chat_worker.start()
        else:
            print("btn enter pressed.")
    
    def message_callback(self, recipient, messages, sender, config):
        sender_name = messages[-1]['name']
        new_text = messages[-1]['content']
        self.tb_chat.append(
            f'\n          -------------------------------------------[{sender_name}]-------------------------------------------'
            + new_text
        )
        return False, None
