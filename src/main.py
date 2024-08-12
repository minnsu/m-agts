from autogen import ConversableAgent, UserProxyAgent

from llms import local_llm_config

# Create the agent that uses the LLM.
assistant = ConversableAgent("agent", llm_config=local_llm_config)

# Create the agent that represents the user in the conversation.
user_proxy = UserProxyAgent("user", code_execution_config=False)

# Let the assistant start the conversation.  It will end when the user types exit.
res = assistant.initiate_chat(user_proxy, message="안녕하세요?")

print(assistant)