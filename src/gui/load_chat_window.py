import json
from copy import deepcopy

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
            clear_history=False,
        )
        self.summary_signal.emit(chat_result.summary)
    
    def message_signal_handler(self, recipient, messages, sender, config):
        self.message_signal.emit(recipient, messages, sender, config)

form_create_edit_chat_class = uic.loadUiType("src/gui/ui/load_chat.ui")[0]
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
        self.is_running = False

        self.chat_worker = None

        self.chat_str = ''
        self.te_chat.setReadOnly(True)

    def _btn_select_config(self):
        self.te_chat.clear()
        self.chat_str = ''
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
        self.te_chat.clear()
        if self.chat_objects:
            self.pte_user_input.setPlainText(self.chat_objects['init_message'])
        self.is_running = False
        self.chat_worker = None

    def _btn_stop(self):
        if self.chat_worker:
            self.chat_str += '<br></br><br></br><span style="color: red">Chatting stopped.</span><br></br><br></br>'
            self.te_chat.setMarkdown(self.chat_str)
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

        if self.is_running == False:
            self.is_running = True
            self.chat_init_and_start(init_message)
        else:
            # TODO: when human_input_mode is 'TERMINATE', 'ALWAYS', processing the input
            print('btn enter pressed')
    
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
        self.chat_str += f'<span style="color: tomato; font-size: 16px">{sender_name}</span><br></br>' + new_text + '<br></br><br></br>'
        self.te_chat.setMarkdown(self.chat_str)
    
    def summary_append_handler(self, summary):
        """
        Main thread function to append summary to the chat window.
        """
        self.chat_str += f'<span style="color: green; font-size: 16px">Summary</span><br></br>' + summary
        self.te_chat.setMarkdown(self.chat_str)
        self.is_running = False

    def chat_init_and_start(self, init_message):
        self.chat_worker = ChatWorker(self.chat_objects, init_message)
        self.chat_worker.message_signal.connect(self.message_append_handler)
        self.chat_worker.summary_signal.connect(self.summary_append_handler)
        self.chat_worker.start()