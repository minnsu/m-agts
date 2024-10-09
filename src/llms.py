import autogen
from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor

def make_agent(agent_config, message_callback):
    code_executor = False
    if agent_config['code_execution_config']:
        executor_type = agent_config['code_execution_config']['executor']
        if executor_type != "None":
            if executor_type == "LocalCommandLineCodeExecutor":
                code_executor = LocalCommandLineCodeExecutor(
                    timeout=10,
                    work_dir=agent_config['code_execution_config']['work_dir'],
                )
            elif executor_type == "DockerCommandLineCodeExecutor":
                code_executor = DockerCommandLineCodeExecutor(
                    timeout=10,
                    work_dir=agent_config['code_execution_config']['work_dir'],
                )
    if code_executor:
        code_executor = {'executor': code_executor}
    agent = ConversableAgent(
        name=agent_config['name'],
        system_message=agent_config['system_message'],
        llm_config=agent_config['llm_config'],
        code_execution_config=code_executor,
        human_input_mode=agent_config['human_input_mode'],
    )
    agent.register_reply(
        [autogen.Agent, None],
        reply_func=message_callback,
        config={"callback": None}
    )
    return agent

def make_agents(agents_list, message_callback):
    agents = []
    for agent_config in agents_list:
        agent = make_agent(agent_config, message_callback)
        agents.append(agent)
    return agents

def find_agent(agents_list, agent_name):
    for agent in agents_list:
        if agent._name == agent_name:
            return agent
    return None

def make_chat(chat_config, message_callback):
    agents_list = make_agents(chat_config['agents_list'], message_callback)
    
    chat_objects = {}
    if len(agents_list) == 2 and chat_config['recipient'] != "GroupChatManager":
        initiator = find_agent(agents_list, chat_config['initiator_agent'])
        recipient = find_agent(agents_list, chat_config['recipient'])
        chat_objects['recipient'] = recipient
    else:
        group_chat = GroupChat(
            agents=agents_list,
            messages=[],
            max_round=chat_config['max_round']+1,
            allow_repeat_speaker=False,
        )
        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=chat_config['group_chat_manager_llm_config'],
        )
        initiator = find_agent(agents_list, chat_config['initiator_agent'])
        chat_objects['recipient'] = group_chat_manager
    
    chat_objects['initiator_agent'] = initiator
    chat_objects['init_message'] = chat_config['init_message']
    chat_objects['summary_method'] = chat_config['summary_method']
    
    return chat_objects
