from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5 import uic

form_create_edit_chat_class = uic.loadUiType("ui/create_edit_chat.ui")[0]
class CreateEditChat(QDialog, form_create_edit_chat_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # LLM Configs
        self.btn_select_llm_config.clicked.connect(self._btn_select_llm_config)
        self.btn_edit_llm_config.clicked.connect(self._btn_edit_llm_config)

        # Agent Configs
        self.btn_advanced_llm_config.clicked.connect(self._btn_advanced_llm_config)
        self.btn_add_tool.clicked.connect(self._btn_add_tool)
        self.btn_save_agent.clicked.connect(self._btn_save_agent)

        # Entire Chat Configs
        self.btn_load_config.clicked.connect(self._btn_load_config)
        self.btn_save_config.clicked.connect(self._btn_save_config)

        self.agents = {}
        self.llm_config_list = {}

        # TODO: cb_agents 변경에 따라 값 변경하도록 구현 추가해야 함. - event handler 추가

    def _btn_select_llm_config(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_llm_config_path.setText(fname[0])

        self.llm_config_list = {}
        
        # TODO: 파일을 읽어서 cb_llm_config에 추가해야 함 + self.llm_config_list에 추가해야 하여 저장 시 함께 저장되도록

    def _btn_edit_llm_config(self):
        self.edit_llm_config = EditLLMConfig()
        self.edit_llm_config.exec()

    def _btn_advanced_llm_config(self):
        self.advanced_llm_config = AdvancedLLMConfig()
        self.advanced_llm_config.exec()

    def _btn_add_tool(self):
        print("Error: Not Implemented [CreateEditChat._btn_add_tool]")

    def _btn_save_agent(self):
        agent_config = {
            "name": self.le_name.text(),
            "system_message": self.pte_system_message.toPlainText(),
            "llm_config": self.cb_llm_config.currentText(),
            "human_input_mode": self.cb_human_input_mode.currentText(),
            "code_execution_config": {
                "executor": self.cb_code_execution.currentText(),
                "work_dir": self.le_code_execution.text(),
            },
            "tools": self.cb_tools.currentText(),
        }
        # print(agent_config)
        self.agents[agent_config["name"]] = agent_config

        self.cb_agents.addItem(agent_config["name"])
        self.cb_initiator_agent.addItem(agent_config["name"])
        self.cb_recipient.addItem(agent_config["name"])

        self.clear_inputs(mode='agent')
        self.cb_agents.setCurrentIndex(0)

    def _btn_load_config(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_chat_config_path.setText(fname[0])
        
        # TODO: 파일을 읽어서 각 값을 세팅해야 함
        # llm_config_list ~ init_message까지

    def _btn_save_config(self):
        chat_config = {
            "llm_config_list": self.llm_config_list,
            "agents": self.agents,

            "initiator_agent": self.cb_initiator_agent.currentText(),
            "recipient": self.cb_recipient.currentText(),
            "max_round": int(self.le_max_turns.text()),
            "summary_method": self.cb_summary_method.currentText(),
            "init_message": self.pte_init_message.toPlainText(),
        }

        dir_path = QFileDialog.getExistingDirectory(self)
        self.clear_inputs(mode='chat')
        # TODO: dir_path/chat_config.json으로 파일을 저장
    
    def clear_inputs(self, mode='all'):
        if mode == 'agent':
            self.le_name.clear()
            self.pte_system_message.clear()
            self.le_code_execution.clear()
        elif mode == 'chat':
            self.agents = {}
            self.cb_agents.clear()
            self.cb_initiator_agent.clear()
            self.cb_recipient.clear()
            self.cb_recipient.addItem("GroupChatManager")
            self.le_max_turns.setText("10")
            self.pte_init_message.clear()


form_edit_llm_config_class = uic.loadUiType("ui/edit_llm_config.ui")[0]
class EditLLMConfig(QDialog, form_edit_llm_config_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_add_llm_config.clicked.connect(self._btn_add_llm_config)

        # TODO: cb_llm_config 변경에 따른 값 변경 구현 추가해야 함 ~ cb_agents와 비슷한 방식으로

    def _btn_add_llm_config(self):
        try:
            llm_config = {
                "model": self.le_model.text(),
                "api_key": self.le_api_key.text(),
                "api_type": self.le_api_type.text(),
                "tags": [tag.strip() for tag in self.le_tags.text().split(",") if len(self.le_tags.text()) > 0],
                "base_url": self.le_base_url.text(),
            }
            if self.le_price_input.text() != "" and self.le_price_output.text() != "":
                llm_config["price"] = [float(self.le_price_input.text()), float(self.le_price_output.text())],

            print(llm_config)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Input type")
        
        # TODO: llm_config_list에 추가해야 하고, CreateEditChat의 llm_config_list에도 동기화
        

form_advanced_llm_config_class = uic.loadUiType("ui/advanced_llm_config.ui")[0]
class AdvancedLLMConfig(QDialog, form_advanced_llm_config_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_set.clicked.connect(self._btn_set)

    def _btn_set(self):
        try:
            advanced_llm_config = {
                "temperature": float(self.le_temperature.text()),
                "top_p": float(self.le_top_p.text()),
                "timeout": int(self.le_timeout.text()),
                "max_tokens": int(self.le_max_tokens.text()),
            }
            print(advanced_llm_config)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Input type")
        
        # TODO: 값이 존재한다면 agent의 llm_config의 형식이 달라질 수 있음을 고려하여 수정해야 함
        # {"llm_config": 기존, "temperature": float, "top_p": float, "timeout": int, "max_tokens": int}와 같이?
        # 문서 확인하여 최대한 비슷하게 구현할 것