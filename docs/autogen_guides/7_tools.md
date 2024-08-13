# Tool
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
