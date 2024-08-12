# AutoGen 사용법

### llm_config (https://microsoft.github.io/autogen/docs/topics/llm_configuration)
```python
import os
llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}],
}

import autogen
assistant = autogen.AssistantAgent(name="assistant", llm_config=llm_config)
```
- 에이전트 생성자에 전달하여 해당 LLM을 사용한다.

- ```config_list```
    ```python
    [
        {
            "model": "gpt-4",
            "api_key": os.environ['OPENAI_API_KEY']
        }
    ]
    ```
    - model (str, 필수): 'gpt-4', 'gpt-3.5-turbo'와 같은 사용할 모델 이름
    - api_key (str, 선택): 모델 API 엔드포인트에 접근하기 위한 API KEY
    - base_url (str, 선택): API 엔드포인트의 base url
    - tags (List[str], 선택): 필터링을 위해 사용할 수 있는 tags
- ```autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST",)```
    ```python
    config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST",
    )

    # Then, create the assistant agent with the config list
    assistant = autogen.AssistantAgent(name="assistant", llm_config={"config_list": config_list})
    ```
    - 환경변수로 지정된 경로에서 파일 로드 시도
    - 파일 없으면 환경 변수를 JSON 문자열로 해석 시도
    - 지정된 경로에 있는 파일 해석 시도
- ```filtered_dict```
    ```python
    filter_dict = {"model": ["gpt-3.5-turbo"]}

    config_list = autogen.filter_config(config_list, filter_dict)
    # or
    config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST", filter_dict=filter_dict)
    ```
    - 기준에 따라 필터링한다.
- example
    ```python
    llm_config = {
        "config_list": [
            {
                "model": "my-gpt-4-deployment",
                "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
                "api_type": "azure",
                "base_url": os.environ.get("AZURE_OPENAI_API_BASE"),
                "api_version": "2024-02-01",
            },
            {
                "model": "llama-7B",
                "base_url": "http://127.0.0.1:8080",
                "api_type": "openai",
            },
        ],
        "temperature": 0.9,
        "timeout": 300,
    }
    ```


### ConversableAgent
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


### 에이전트 간의 대화 종료
- 작업이 완료되거나 리소스 낭비를 예방하기 위해 적절하게 종료해야 한다.
- 2가지의 대화 종료 방법이 있다.
    1. ```initiate_chat```의 매개변수 지정
    2. 에이전트 자체에 종료 트리거 설정
- ```initiate_chat```
    ```python
    result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)
    ```
    - ```max_turns=int```를 사용하여 최대 대화 길이를 설정할 수 있다.
- 에이전트 트리거
    ```python
    joe = ConversableAgent(
        "joe",
        system_message="Your name is Joe and you are a part of a duo of comedians.",
        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
        human_input_mode="NEVER",  # Never ask for human input.
        max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
        is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
    )

    result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.")
    ```
    - ```max_consecutive_auto_reply```: 같은 발신자에 대한 자동 응답의 최대 개수를 지정하며, 이를 초과하면 종료를 트리거한다.
    - ```is_termination_msg```: 수신된 메시지가 특정 조건을 충족하면 종료를 트리거한다.

### Human Feedback 지정하기
- 3가지
    1. ```NEVER```: 사람의 피드백을 요청하지 않는다.
    2. ```TERMINATE```: 종료 조건이 충족될 때 사람의 피드백을 요청한다. 답장을 수행하면 대화가 계속된다.
    3. ```ALWAYS```: 항상 사람의 피드백을 요청한다. 매번 건너뛰거나 답장을 하거나 대화를 종료할 수 있다.

### Code Executor
- 2가지 내장 코드 실행기가 존재
    1. Command line
        - [```LocalCommandLineCodeExecutor```](https://microsoft.github.io/autogen/docs/reference/coding/local_commandline_code_executor#localcommandlinecodeexecutor)
        - [```DockerCommandLineCodeExecutor```](https://microsoft.github.io/autogen/docs/reference/coding/docker_commandline_code_executor#dockercommandlinecodeexecutor)
    2. Jupyter Kernel
        - [```jupyter.JupyterCodeExecutor```](https://microsoft.github.io/autogen/docs/reference/coding/jupyter/jupyter_code_executor#jupytercodeexecutor)
- ```LocalCommandLineCodeExecutor``` example
    ```python
    import tempfile

    from autogen import ConversableAgent
    from autogen.coding import LocalCommandLineCodeExecutor

    # Create a temporary directory to store the code files.
    temp_dir = tempfile.TemporaryDirectory()

    # Create a local command line code executor.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
    )

    # Create an agent with code executor configuration.
    code_executor_agent = ConversableAgent(
        "code_executor_agent",
        llm_config=False,  # Turn off LLM for this agent.
        code_execution_config={"executor": executor},  # Use the local command line code executor.
        human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
    )

    message_with_code_block = """This is a message with code block.
    The code block is below:
    
    python
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.random.randint(0, 100, 100)
    y = np.random.randint(0, 100, 100)
    plt.scatter(x, y)
    plt.savefig('scatter.png')
    print('Scatter plot saved to scatter.png')
    
    This is the end of the message.
    """

    # Generate a reply for the given code.
    reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
    print(reply)
    ```
- ```DockerCommandLineCodeExecutor``` example
    ```python
    from autogen.coding import DockerCommandLineCodeExecutor

    # Create a temporary directory to store the code files.
    temp_dir = tempfile.TemporaryDirectory()

    # Create a Docker command line code executor.
    executor = DockerCommandLineCodeExecutor(
        image="python:3.12-slim",  # Execute code using the given docker image name.
        timeout=10,  # Timeout for each code execution in seconds.
        work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
    )

    # Create an agent with code executor configuration that uses docker.
    code_executor_agent_using_docker = ConversableAgent(
        "code_executor_agent_docker",
        llm_config=False,  # Turn off LLM for this agent.
        code_execution_config={"executor": executor},  # Use the docker command line code executor.
        human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
    )

    # When the code executor is no longer used, stop it to release the resources.
    # executor.stop()
    ```


### [UserProxyAgent](https://microsoft.github.io/autogen/docs/reference/agentchat/user_proxy_agent#userproxyagent)
- ```human_input_mode="ALWAYS"```, ```llm_config=False```로 설정된 ```ConversableAgent```이다.
- 즉, 항상 사람의 입력을 요청하고, LLM을 사용하지 않는다. 

### [AssistantAgent](https://microsoft.github.io/autogen/docs/reference/agentchat/assistant_agent#assistantagent)
- ```human_input_mode="NEVER"```, ```code_execution_config=False```로 설정된 ```ConversableAgent```이다.
- 즉, 사람의 입력 대신 LLM을 사용해 생성하며, 코드를 실행하지 않는다.
- default system message가 존재한다.
    ```
    ('You are a helpful AI assistant.\n'
    'Solve tasks using your coding and language skills.\n'
    'In the following cases, suggest python code (in a python coding block) or '
    'shell script (in a sh coding block) for the user to execute.\n'
    '    1. When you need to collect info, use the code to output the info you '
    'need, for example, browse or search the web, download/read a file, print the '
    'content of a webpage or a file, get the current date/time, check the '
    'operating system. After sufficient info is printed and the task is ready to '
    'be solved based on your language skill, you can solve the task by yourself.\n'
    '    2. When you need to perform some task with code, use the code to perform '
    'the task and output the result. Finish the task smartly.\n'
    'Solve the task step by step if you need to. If a plan is not provided, '
    'explain your plan first. Be clear which step uses code, and which step uses '
    'your language skill.\n'
    'When using code, you must indicate the script type in the code block. The '
    'user cannot provide any other feedback or perform any other action beyond '
    "executing the code you suggest. The user can't modify your code. So do not "
    "suggest incomplete code which requires users to modify. Don't use a code "
    "block if it's not intended to be executed by the user.\n"
    'If you want the user to save the code in a file before executing it, put # '
    "filename: <filename> inside the code block as the first line. Don't include "
    'multiple code blocks in one response. Do not ask users to copy and paste the '
    "result. Instead, use 'print' function for the output when relevant. Check "
    'the execution result returned by the user.\n'
    'If the result indicates there is an error, fix the error and output the code '
    'again. Suggest the full code instead of partial code or code changes. If the '
    "error can't be fixed or if the task is not solved even after the code is "
    'executed successfully, analyze the problem, revisit your assumption, collect '
    'additional info you need, and think of a different approach to try.\n'
    'When you find an answer, verify the answer carefully. Include verifiable '
    'evidence in your response if possible.\n'
    'Reply "TERMINATE" in the end when everything is done.\n'
    '    ')
    ```


### Tool
- 에이전트가 사용할 수 있는 미리 정의된 기능이며, 임의의 코드를 작성하는 대신 도구를 호출하여 웹 검색, 계산, 파일 읽기, API 호출 등을 수행할 수 있다.
- 파이썬 함수를 사용해 생성할 수 있다.
    ```python
    from typing import Annotated, Literal

    Operator = Literal["+", "-", "*", "/"]


    def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            return int(a / b)
        else:
            raise ValueError("Invalid operator")
    ```
    - type hint를 사용하여 에이전트에게 정보를 제공해야 한다.
- 에이전트에 다음과 같이 등록한다.
    ```python
    import os

    from autogen import ConversableAgent

    # Let's first define the assistant agent that suggests tool calls.
    assistant = ConversableAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. "
        "You can help with simple calculations. "
        "Return 'TERMINATE' when the task is done.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    )

    # The user proxy agent is used for interacting with the assistant agent
    # and executes tool calls.
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    # Register the tool signature with the assistant agent.
    assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

    # Register the tool function with the user proxy agent.
    user_proxy.register_for_execution(name="calculator")(calculator)
    ```
    - ```register_for_llm```을 통해 llm이 해당 도구를 사용할 수 있는 명령어를 생성하도록 한다.
    - ```register_for_execution```을 통해 요청된 명령을 실행하도록 한다.
    ```python
    from autogen import register_function

    # Register the calculator function to the two agents.
    register_function(
        calculator,
        caller=assistant,  # The assistant agent can suggest calls to the calculator.
        executor=user_proxy,  # The user proxy agent can execute the calculator calls.
        name="calculator",  # By default, the function name is used as the tool name.
        description="A simple calculator",  # A description of the tool.
    )
    ```
    - 이와 같이 동시에 등록할 수 있다.
- ```pydantic```을 사용해 복잡한 스키마를 제공할 수 있다.
    ```python
    from pydantic import BaseModel, Field


    class CalculatorInput(BaseModel):
        a: Annotated[int, Field(description="The first number.")]
        b: Annotated[int, Field(description="The second number.")]
        operator: Annotated[Operator, Field(description="The operator.")]


    def calculator(input: Annotated[CalculatorInput, "Input to the calculator."]) -> int:
        if input.operator == "+":
            return input.a + input.b
        elif input.operator == "-":
            return input.a - input.b
        elif input.operator == "*":
            return input.a * input.b
        elif input.operator == "/":
            return int(input.a / input.b)
        else:
            raise ValueError("Invalid operator")
    ```