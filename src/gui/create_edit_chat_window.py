import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5 import uic

form_create_edit_chat_class = uic.loadUiType("gui/ui/create_edit_chat.ui")[0]
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

        self.agents_list = []

        self.llm_config_list_path = ""
        self.llm_config_list = []

        self.cb_agents.currentIndexChanged.connect(self.on_cb_agents_changed)

    def _btn_select_llm_config(self):
        """
        Select LLM Config file

        Read the file and set the values to the LLM Config list
        """
        fname = QFileDialog.getOpenFileName(self)
        self.label_llm_config_path.setText(fname[0])
        self.llm_config_list_path = fname[0]

        with open(fname[0], 'r') as f:
            self.llm_config_list = json.load(f)
        
        self.cb_llm_config.clear()
        for llm_config in self.llm_config_list:
            self.cb_llm_config.addItem(llm_config["model"])
        self.cb_llm_config.setCurrentIndex(0)

    def _btn_edit_llm_config(self):
        """
        Open edit LLM Config window

        After editing, save the values to the LLM Config list and file.
        """
        self.edit_llm_config = EditLLMConfig(self)
        self.edit_llm_config.exec()

        with open(self.llm_config_list_path, 'w') as f:
            json.dump(self.llm_config_list, f, indent=4)
        
        self.cb_llm_config.clear()
        for llm_config in self.llm_config_list:
            self.cb_llm_config.addItem(llm_config["model"])

    def _btn_advanced_llm_config(self):
        self.advanced_llm_config = AdvancedLLMConfig()
        self.advanced_llm_config.exec()

    def _btn_add_tool(self):
        print("Error: Not Implemented [CreateEditChat._btn_add_tool]")

    def on_cb_agents_changed(self, index):
        """
        Combobox index changed event handler

        if index is 0, clear all inputs and do nothing
        else, set the values of the selected Agent Config
        """
        self.clear_inputs(mode='agent')

        if index == 0:
            pass
        elif self.cb_agents.count() > 0:
            target = self.agents_list[index-1]
            self.le_name.setText(target["name"])
            self.pte_system_message.setPlainText(target["system_message"])
            self.cb_llm_config.setCurrentIndex(self.llm_config_list.index(target["llm_config"]))
            self.cb_human_input_mode.setCurrentIndex(["NEVER", "ALWAYS", "TERMINATE"].index(target["human_input_mode"]))
            self.cb_code_execution.setCurrentIndex(["None", "LocalCommandLineCodeExecutor", "DockerCommandLineCodeExecutor"].index(target["code_execution_config"]["executor"]))
            self.le_code_execution.setText(target["code_execution_config"]["work_dir"])

    def _btn_save_agent(self):
        """
        Add or Edit Agent Config
        """
        agent_config = {
            "name": self.le_name.text(),
            "system_message": self.pte_system_message.toPlainText(),
            "llm_config": self.llm_config_list[self.cb_llm_config.currentIndex()],
            "human_input_mode": self.cb_human_input_mode.currentText(),
            "code_execution_config": {
                "executor": self.cb_code_execution.currentText() if self.cb_code_execution.currentText() != "None" else "None",
                "work_dir": self.le_code_execution.text(),
            },
            "tools": self.cb_tools.currentText(),
        }
        if self.cb_agents.currentIndex() == 0:
            self.agents_list.append(agent_config)
            self.cb_agents.addItem(agent_config["name"])
            self.cb_initiator_agent.addItem(agent_config["name"])
            self.cb_recipient.addItem(agent_config["name"])
        else:
            self.agents_list[self.cb_agents.currentIndex()-1] = agent_config

        self.clear_inputs(mode='agent')
        self.cb_agents.setCurrentIndex(0)
        self.on_cb_agents_changed(0)

    def _btn_load_config(self):
        """
        Load Chat Config file
        """
        fname = QFileDialog.getOpenFileName(self)
        self.label_chat_config_path.setText(fname[0])
        self.clear_inputs(mode='all')

        with open(fname[0], 'r') as f:
            chat_config = json.load(f)
        
        self.llm_config_list_path = chat_config["llm_config_list_path"]
        self.label_llm_config_path.setText(self.llm_config_list_path)

        self.llm_config_list = chat_config["llm_config_list"]
        for llm_config in self.llm_config_list:
            self.cb_llm_config.addItem(llm_config["model"])

        self.agents_list = chat_config["agents_list"]
        for agent in self.agents_list:
            self.cb_agents.addItem(agent["name"])
            self.cb_initiator_agent.addItem(agent["name"])
            self.cb_recipient.addItem(agent["name"])

        self.cb_initiator_agent.setCurrentIndex(self.cb_initiator_agent.findText(chat_config["initiator_agent"]))
        self.cb_recipient.setCurrentIndex(self.cb_recipient.findText(chat_config["recipient"]))
        self.le_max_turns.setText(str(chat_config["max_round"]))
        self.cb_summary_method.setCurrentIndex(["last_msg", "reflection_with_llm"].index(chat_config["summary_method"]))
        self.pte_init_message.setPlainText(chat_config["init_message"])

    def _btn_save_config(self):
        """
        Save Chat Config file
        """
        try:
            chat_config = {
                "llm_config_list_path": self.llm_config_list_path,
                "llm_config_list": self.llm_config_list,
                "agents_list": self.agents_list,

                "initiator_agent": self.cb_initiator_agent.currentText(),
                "recipient": self.cb_recipient.currentText(),
                "group_chat_manager_llm_config": self.llm_config_list[self.cb_llm_config.currentIndex()] if self.cb_recipient.currentText() == "GroupChatManager" else None,
                "max_round": int(self.le_max_turns.text()),
                "summary_method": self.cb_summary_method.currentText(),
                "init_message": self.pte_init_message.toPlainText(),
            }
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Input type")

        dir_path = QFileDialog.getExistingDirectory(self)
        self.clear_inputs(mode='chat')
        self.label_chat_config_path.setText("Selected chat config file path")

        with open(f"{dir_path}/chat_config.json", 'w') as f:
            json.dump(chat_config, f, indent=4)
    
    def clear_inputs(self, mode='all'):
        if mode=='agent':
            self.le_name.clear()
            self.pte_system_message.clear()
            if self.cb_llm_config.count() > 0:
                self.cb_llm_config.setCurrentIndex(0)
            self.cb_human_input_mode.setCurrentIndex(0)
            self.cb_code_execution.setCurrentIndex(0)
            self.le_code_execution.clear()
        if mode == 'chat' or mode == 'all':
            self.llm_config_list_path = ""
            self.llm_config_list = []
            self.cb_llm_config.clear()

            self.agents_list = []
            self.cb_agents.clear()
            self.cb_agents.addItem("Make new agent")
            self.cb_initiator_agent.clear()
            self.cb_recipient.clear()
            self.cb_recipient.addItem("GroupChatManager")
            self.le_max_turns.setText("10")
            self.cb_summary_method.setCurrentIndex(0)
            self.pte_init_message.clear()


form_edit_llm_config_class = uic.loadUiType("gui/ui/edit_llm_config.ui")[0]
class EditLLMConfig(QDialog, form_edit_llm_config_class):
    def __init__(self, _parent) :
        super().__init__()
        self.setupUi(self)

        self.btn_edit_llm_config.clicked.connect(self._btn_edit_llm_config)

        self._parent = _parent
        self.llm_config_list = _parent.llm_config_list

        self.cb_llm_config.clear()
        self.cb_llm_config.addItem("Add New LLM Config")
        for llm_config in self.llm_config_list:
            self.cb_llm_config.addItem(llm_config["model"])
        
        self.cb_llm_config.currentIndexChanged.connect(self.on_cb_llm_config_changed)

    def on_cb_llm_config_changed(self, index):
        """
        Combobox index changed event handler

        if index is 0, clear all inputs and do nothing
        else, set the values of the selected LLM Config
        """
        self.le_model.clear()
        self.le_api_key.clear()
        self.le_api_type.clear()
        self.le_tags.clear()
        self.le_base_url.clear()
        self.le_price_input.clear()
        self.le_price_output.clear()

        if index == 0:
            pass
        else:
            target = self.llm_config_list[index-1]
            self.le_model.setText(target["model"] if "model" in target else "")
            self.le_api_key.setText(target["api_key"] if "api_key" in target else "")
            self.le_api_type.setText(target["api_type"] if "api_type" in target else "")
            self.le_tags.setText(", ".join(target["tags"]) if "tags" in target else "")
            self.le_base_url.setText(target["base_url"] if "base_url" in target else "")
            if "price" in target:
                self.le_price_input.setText(str(target["price"][0] if "price" in target else ""))
                self.le_price_output.setText(str(target["price"][1] if "price" in target else ""))

    def _btn_edit_llm_config(self):
        """
        Add or Edit LLM Config

        if index is 0, add new LLM Config
        else, edit the selected LLM Config
        """
        try:
            llm_config = {
                "model": self.le_model.text(),
                "api_key": self.le_api_key.text(),
                "api_type": self.le_api_type.text(),
                "tags": [tag.strip() for tag in self.le_tags.text().split(",") if len(self.le_tags.text()) > 0],
                "base_url": self.le_base_url.text(),
            }
            if self.le_price_input.text() != "" and self.le_price_output.text() != "":
                llm_config["price"] = [float(self.le_price_input.text()), float(self.le_price_output.text())]

            if self.cb_llm_config.currentIndex() == 0:
                self._parent.llm_config_list.append(llm_config)
                self.llm_config_list = self._parent.llm_config_list
                self.cb_llm_config.addItem(llm_config["model"])
            else:
                self._parent.llm_config_list[self.cb_llm_config.currentIndex()-1] = llm_config
                self.llm_config_list = self._parent.llm_config_list
            self.cb_llm_config.setCurrentIndex(0)
            self.on_cb_llm_config_changed(0)

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Input type")

form_advanced_llm_config_class = uic.loadUiType("gui/ui/advanced_llm_config.ui")[0]
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