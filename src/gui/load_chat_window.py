import json

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtWidgets

import autogen
from autogen import ConversableAgent, GroupChat, GroupChatManager

from llms import make_chat

class ChatWorker(QThread):
    message_signal = pyqtSignal(object, list, object, object)
    summary_signal = pyqtSignal(str)

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
        self.summary_signal.emit(chat_result.summary)
    
    def message_signal_handler(self, recipient, messages, sender, config):
        self.message_signal.emit(recipient, messages, sender, config)

form_create_edit_chat_class = uic.loadUiType("gui/ui/load_chat.ui")[0]
class LoadChat(QDialog, form_create_edit_chat_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_select_config.clicked.connect(self._btn_select_config)
        self.btn_reset.clicked.connect(self._btn_reset)
        self.btn_stop.clicked.connect(self._btn_stop)
        self.btn_enter.clicked.connect(self._btn_enter)

        self.pte_user_input.keyPressEvent = self.keyPressEvent

        self.chat_config = None
        self.chat_objects = None
        self.chat_start_flag = False

        self.chat_worker = None

    def _btn_select_config(self):
        self.tb_chat.clear()
        self.pte_user_input.clear()

        fname = QFileDialog.getOpenFileName(self)
        self.label_config_path.setText(fname[0])
        
        print(fname[0])
        with open(fname[0], 'r') as f:
            self.chat_config = json.load(f)
            print(self.chat_config)

        self.chat_objects = make_chat(self.chat_config, self.message_callback)
        self.pte_user_input.setPlainText(self.chat_objects['init_message'])

    def _btn_reset(self):
        self.tb_chat.clear()
        if self.chat_objects:
            self.pte_user_input.setPlainText(self.chat_objects['init_message'])
        self.chat_start_flag = False
        self.chat_worker = None

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
            self.chat_worker.message_signal.connect(self.message_append_handler)
            self.chat_worker.summary_signal.connect(self.summary_append_handler)
            self.chat_worker.start()
        else:
            print("btn enter pressed.")
    
    def message_callback(self, recipient, messages, sender, config):
        """
        This function is called when a message is sent from one agent to another
        """
        self.chat_worker.message_signal_handler(recipient, messages, sender, config)
        return False, None
    
    def message_append_handler(self, recipient, messages, sender, config):
        """
        Main thread function to append messages to the chat window.
        Called from ChatWorker.message_signal_handler
        """
        sender_name = messages[-1]['name']
        new_text = messages[-1]['content']
        self.tb_chat.append(
            f'          -------------------------------------------[{sender_name}]-------------------------------------------\n'
            + new_text
        )
    
    def summary_append_handler(self, summary):
        """
        Main thread function to append summary to the chat window.
        """
        self.tb_chat.append(
            f'          -------------------------------------------[Summary]-------------------------------------------\n'
            + summary
        )
