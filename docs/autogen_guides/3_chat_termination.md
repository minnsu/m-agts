# 에이전트 간의 대화 종료
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
