import os
import sys
import json
from autogen import Agent, ConversableAgent, UserProxyAgent, AssistantAgent, GroupChatManager

def make_llm_config():
    """
    LLM에 대한 설정을 만듭니다.
    """
    model = input("모델 이름을 입력하세요: ")
    api_key = input("API 키를 입력하세요. (없으면 빈 문자열 입력): ")
    if not api_key:
        api_key = "NotRequired"

    config = {
        "model": model,
        "api_key": api_key
    }
    return config

def make_agent(option: int):
    """
    에이전트를 만듭니다.
    """
    print('--- 에이전트 생성 ---')

    config = {}

    name = input("에이전트 이름을 입력하세요: ")
    system_message = input("시스템 메시지를 입력하세요: ")
    llm_config = make_llm_config()

    print("사용자 입력 모드를 선택하세요.", end=" ")
    if option == 1:
        agent_type = "ConversableAgent"
        human_input_mode = input("NEVER, ALWAYS, TERMINATE(기본): ")
    elif option == 2:
        agent_type = "UserProxyAgent"
        human_input_mode = input("NEVER, ALWAYS(기본), TERMINATE: ")
    elif option == 3:
        agent_type = "AssistantAgent"
        human_input_mode = input("NEVER(기본), ALWAYS, TERMINATE: ")

    config["type"] = agent_type
    config["name"] = name
    config["system_message"] = system_message
    config["llm_config"] = llm_config
    config["human_input_mode"] = human_input_mode

    """
    is_termination_msg: Optional[Callable[[Dict], bool]] = None,
    max_consecutive_auto_reply: Optional[int] = None,
    function_map: Optional[Dict[str, Callable]] = None,
    code_execution_config: Union[Dict, Literal[False]] = False,
    default_auto_reply: Union[str, Dict] = "",
    description: Optional[str] = None,
    chat_messages: Optional[Dict[Agent, List[Dict]]] = None,
    """
    return config

def make_agent_config():
    """
    에이전트에 대한 설정을 만듭니다.
    """

    agents = []
    while True:
        option = input("에이전트 유형을 선택하세요.\n1. ConversableAgent\n2. UserProxyAgent\n3. AssistantAgent\n4. 종료\n")
        if int(option) <= 3:
            agents.append(make_agent(int(option)))
        elif option == "4":
            break
        else:
            print("잘못된 입력입니다.")
    
    return agents

def make_chat_config():
    """
    채팅에 대한 설정을 만듭니다.
    """
    
    """
    initiate_agent: Agent,
    receive_agent: Agent,
    init_message: str,
    summary_method: Optional[Callable[[List[str]], str]] = None,
    cache: Optional[Dict] = None,
    """

    chat = {}
    chat["initiate_agent"] = input("채팅을 시작할 에이전트 이름을 입력하세요: ")
    chat["receive_agent"] = input("받을 에이전트 이름을 입력하세요(GroupChat의 경우 빈칸 입력): ")
    chat["init_message"] = input("시작 메시지를 입력하세요: ")
    chat["max_round"] = input("최대 라운드 수를 입력하세요: ")
    # chat["summary_method"] = input("요약 방법을 입력하세요: ")

    return chat

def make_config():
    """
    설정을 만듭니다.
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path = input(f"[{cur_dir}]설정 파일을 저장할 경로를 입력하세요: ")
    
    config = {}
    config['agent'] = make_agent_config()
    config['chat'] = make_chat_config()

    with open(path, 'w') as f:
        json.dump(config, f)

# --------------------------------------------------

def load_chat_config(path: str=None) -> dict:
    """
    채팅 설정을 로드합니다.
    """
    pass

def load_config(path: str=None):
    """
    설정을 로드합니다.

    먼저 llm_config를 load하고, 그 다음 agent_config를 load합니다.
    chat_config를 load하기 위해서는 agent 객체가 필요하므로 가장 마지막에 load합니다.

    """
    while not path:
        path = input("설정 파일 경로를 입력하세요: ")
        if not os.path.exists(path):
            print("경로가 존재하지 않습니다.")
            path = None
    
    chat_config = load_chat_config(path)

    initiate_agent = chat_config["initiate_agent"]
    receive_agent = chat_config["receive_agent"]
    init_message = chat_config["init_message"]
    
    initiate_agent.initiate_chat(
        recipient=receive_agent,
        messages=[init_message],
        summary_method=chat_config["summary_method"],
        cache=None
    )

def main():
    """
    메인 UI 함수입니다.
    """
    while True:
        option = input("1. 설정 만들기\n2. 설정 로드하기\n3. 종료\n")
        if option == "1":
            make_config()
        elif option == "2":
            load_config()
        elif option == "3":
            break
        else:
            print("잘못된 입력입니다.")