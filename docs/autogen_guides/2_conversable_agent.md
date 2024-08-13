# ConversableAgent
```python
import os

from autogen import ConversableAgent

agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)
```
- 대화를 수행하는 에이전트를 생성한다.
- ```generate_reply```
    ```python
    reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
    print(reply)
    ```
    ```python
    Sure, here's a light-hearted joke for you:

    Why don't scientists trust atoms?

    Because they make up everything!
    ```
- ```system_message```를 통해 역할을 할당할 수 있다.
    ```python
    cathy = ConversableAgent(
        "cathy",
        system_message="Your name is Cathy and you are a part of a duo of comedians.",
        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
        human_input_mode="NEVER",  # Never ask for human input.
    )

    joe = ConversableAgent(
        "joe",
        system_message="Your name is Joe and you are a part of a duo of comedians.",
        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
        human_input_mode="NEVER",  # Never ask for human input.
    )

    result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)
    ```
