# Conversation Pattern
- 다양한 대화 패턴이 존재한다.
    1. Two-Agent Chat
    2. Sequential Chat: 이전 채팅의 요약을 다음 채팅의 context로 가져오는 carryover 메커니즘으로 연결된다.
    3. Group Chat: 2명 이상의 에이전트가 참여한다. 다음에 말할 에이전트를 지정하기 위해 다양한 메소드를 지원한다.
        - ```round_robin```, ```random```, ```manual```, ```auto```
        - 또는 [```speaker_selection_method=custom_func```](https://microsoft.github.io/autogen/docs/topics/groupchat/customized_speaker_selection/)과 같이 지정 가능
- Two-Agent Chat
    ```python
    import os

    from autogen import ConversableAgent

    student_agent = ConversableAgent(
        name="Student_Agent",
        system_message="You are a student willing to learn.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    )
    teacher_agent = ConversableAgent(
        name="Teacher_Agent",
        system_message="You are a math teacher.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    )

    chat_result = student_agent.initiate_chat(
        teacher_agent,
        message="What is triangle inequality?",
        summary_method="reflection_with_llm",
        max_turns=2,
    )
    ```
    - 2개 에이전트 중 ```initiate_chat```을 호출하는 측이 송신, 남은 1개 에이전트가 수신 측이 된다.
    - ```summary_method```를 통해 요약 방식을 설정할 수 있다.
        - 기본 값은 "last_msg"이며, "reflection_with_llm"으로 설정시 llm client를 사용해 요약한다.
            - 먼저 수신 llm을 사용하려고 하고, 실패시 발신 llm을 사용한다.
- Sequential Chat
    - 채팅 자체에 대한 요약을 다음 채팅에서 활용하는 방식으로, 상호의존적인 하위 작업으로 나눠지는 복잡한 작업에서 유용하다.
    ```python
    # The Number Agent always returns the same numbers.
    number_agent = ConversableAgent(
        name="Number_Agent",
        system_message="You return me the numbers I give you, one number each line.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    # The Adder Agent adds 1 to each number it receives.
    adder_agent = ConversableAgent(
        name="Adder_Agent",
        system_message="You add 1 to each number I give you and return me the new numbers, one number each line.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    # The Multiplier Agent multiplies each number it receives by 2.
    multiplier_agent = ConversableAgent(
        name="Multiplier_Agent",
        system_message="You multiply each number I give you by 2 and return me the new numbers, one number each line.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    # The Subtracter Agent subtracts 1 from each number it receives.
    subtracter_agent = ConversableAgent(
        name="Subtracter_Agent",
        system_message="You subtract 1 from each number I give you and return me the new numbers, one number each line.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    # The Divider Agent divides each number it receives by 2.
    divider_agent = ConversableAgent(
        name="Divider_Agent",
        system_message="You divide each number I give you by 2 and return me the new numbers, one number each line.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    # Start a sequence of two-agent chats.
    # Each element in the list is a dictionary that specifies the arguments
    # for the initiate_chat method.
    chat_results = number_agent.initiate_chats(
        [
            {
                "recipient": adder_agent,
                "message": "14",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": multiplier_agent,
                "message": "These are my numbers",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": subtracter_agent,
                "message": "These are my numbers",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "recipient": divider_agent,
                "message": "These are my numbers",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
        ]
    )
    ```
    - 각 채팅의 summary를 수행하는 방법을 지정할 수 있다.
        - "last_msg", "reflection_with_llm"
    ```
    ********************************************************************************
    Start a new chat with the following message: 
    14

    With the following carryover: 


    ********************************************************************************
    Number_Agent (to Adder_Agent):

    14

    --------------------------------------------------------------------------------
    Adder_Agent (to Number_Agent):

    15

    --------------------------------------------------------------------------------
    Number_Agent (to Adder_Agent):

    15

    --------------------------------------------------------------------------------
    Adder_Agent (to Number_Agent):

    16

    --------------------------------------------------------------------------------

    ********************************************************************************
    Start a new chat with the following message: 
    These are my numbers

    With the following carryover: 
    16

    ********************************************************************************
    Number_Agent (to Multiplier_Agent):

    These are my numbers
    Context: 
    16

    --------------------------------------------------------------------------------
    Multiplier_Agent (to Number_Agent):

    32

    --------------------------------------------------------------------------------
    Number_Agent (to Multiplier_Agent):

    32

    --------------------------------------------------------------------------------
    Multiplier_Agent (to Number_Agent):

    64

    --------------------------------------------------------------------------------

    ********************************************************************************
    Start a new chat with the following message: 
    These are my numbers

    With the following carryover: 
    16
    64

    ********************************************************************************
    Number_Agent (to Subtracter_Agent):

    These are my numbers
    Context: 
    16
    64

    --------------------------------------------------------------------------------
    Subtracter_Agent (to Number_Agent):

    15
    63

    --------------------------------------------------------------------------------
    Number_Agent (to Subtracter_Agent):

    15
    63

    --------------------------------------------------------------------------------
    Subtracter_Agent (to Number_Agent):

    14
    62

    --------------------------------------------------------------------------------

    ********************************************************************************
    Start a new chat with the following message: 
    These are my numbers

    With the following carryover: 
    16
    64
    14
    62

    ********************************************************************************
    Number_Agent (to Divider_Agent):

    These are my numbers
    Context: 
    16
    64
    14
    62

    --------------------------------------------------------------------------------
    Divider_Agent (to Number_Agent):

    8
    32
    7
    31

    --------------------------------------------------------------------------------
    Number_Agent (to Divider_Agent):

    8
    32
    7
    31

    --------------------------------------------------------------------------------
    Divider_Agent (to Number_Agent):

    4
    16
    3.5
    15.5

    --------------------------------------------------------------------------------
    ```
    - 이처럼 다음 채팅으로 넘어갈 때에는 이전의 모든 채팅에 대한 context가 함께 제공된다.
    - 이외에도 ```autogen.agentchat.initiate_chats```와 같은 함수 호출을 통해 각 채팅의 발신 에이전트를 지정해줄 수 있다.
- Group Chat
    - 2명 이상의 에이전트를 포함하는 일반적인 대화 패턴을 제공한다. 모든 에이전트가 하나의 대화에 속하여 같은 context를 공유한다.
    - 특수한 에이전트인 ```GroupChatManager```에 의해 만들어진다.
    - ```GroupChatManager```는 말할 에이전트를 선택하여 말하도록 하고, 이 메시지는 다시 ```GroupChatManager```에게 전달되어 다른 에이전트들에게 브로드캐스트된다.
    - 다양한 방법으로 순서를 지정할 수 있다.
        - ```round_robin```: 제공된 순서대로
        - ```random```: 무작위
        - ```manual```: 사람의 입력을 요청
        - ```auto```: Manager의 LLM을 바탕으로 선택
    - ```auto```
        ```python
        # The `description` attribute is a string that describes the agent.
        # It can also be set in `ConversableAgent` constructor.
        adder_agent.description = "Add 1 to each input number."
        multiplier_agent.description = "Multiply each input number by 2."
        subtracter_agent.description = "Subtract 1 from each input number."
        divider_agent.description = "Divide each input number by 2."
        number_agent.description = "Return the numbers given."
        ```
        - ```agent.description```을 바탕으로 선택한다. 없다면 ```system_message```를 사용해 선택한다.
    - ```GroupChat```
        ```python
        from autogen import GroupChat

        group_chat = GroupChat(
            agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
            messages=[],
            max_round=6,
        )
        ```
        - ```messages```는 그룹 채팅의 메시지를 초기화
        - ```max_round```는 최대 6번의 라운드를 수행
        ```python
        from autogen import GroupChatManager

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        chat_result = number_agent.initiate_chat(
            group_chat_manager,
            message="My number is 3, I want to turn it into 13.",
            summary_method="reflection_with_llm",
        )
        ```
        - Manager를 생성할 때, ```group_chat``` 객체를 제공하고, ```auto```를 설정했을 때에는 ```llm_config```를 설정한다.
    - ```send_introductions```
        ```python
        group_chat_with_introductions = GroupChat(
            agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
            messages=[],
            max_round=6,
            send_introductions=True,
        )
        ```
        - Manager는 채팅 시작 전 모든 에이전트에게 각각의 에이전트의 이름과 설명이 포함된 메시지를 전송하여 다른 에이전트에 대한 설명을 제공한다.
    - 연결되는 에이전트 제한하기
        - 특정 에이전트 다음에 허용/비허용되는 에이전트를 매핑하여 제공할 수 있다.
        ```python
        allowed_transitions = {
            number_agent: [adder_agent, number_agent],
            adder_agent: [multiplier_agent, number_agent],
            subtracter_agent: [divider_agent, number_agent],
            multiplier_agent: [subtracter_agent, number_agent],
            divider_agent: [adder_agent, number_agent],
        }

        constrained_graph_chat = GroupChat(
            agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent, number_agent],
            allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=12,
            send_introductions=True,
        )

        constrained_group_chat_manager = GroupChatManager(
            groupchat=constrained_graph_chat,
            llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        chat_result = number_agent.initiate_chat(
            constrained_group_chat_manager,
            message="My number is 3, I want to turn it into 10. Once I get to 10, keep it there.",
            summary_method="reflection_with_llm",
        )
        ```

- Nested Chat
    - 이전의 대화 패턴은 복잡한 워크플로우를 구성하는 데에 좋지만, Q&A, 개인 비서와 같은 하나의 대화 인터페이스처럼 보이진 않는다. 따라서 워크플로우를 하나의 에이전트처럼 패키징하기 위한 방법으로 Nested Chat을 제공한다.
    - 유저의 입력을 트리거 조건에 따라 Nested Chat에 제공할지 결정하고, 트리거하면 Nested Chat이 수행된다. 그리고 최종 결과를 유저에게 반환된다.
    ```python
    import tempfile
    temp_dir = tempfile.gettempdir()

    arithmetic_agent = ConversableAgent(
        name="Arithmetic_Agent",
        llm_config=False,
        human_input_mode="ALWAYS",
        # This agent will always require human input to make sure the code is
        # safe to execute.
        code_execution_config={"use_docker": False, "work_dir": temp_dir},
    )

    code_writer_agent = ConversableAgent(
        name="Code_Writer_Agent",
        system_message="You are a code writer. You write Python script in Markdown code blocks.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    poetry_agent = ConversableAgent(
        name="Poetry_Agent",
        system_message="You are an AI poet.",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        human_input_mode="NEVER",
    )

    nested_chats = [
        {
            "recipient": group_chat_manager_with_intros,
            "summary_method": "reflection_with_llm",
            "summary_prompt": "Summarize the sequence of operations used to turn " "the source number into target number.",
        },
        {
            "recipient": code_writer_agent,
            "message": "Write a Python script to verify the arithmetic operations is correct.",
            "summary_method": "reflection_with_llm",
        },
        {
            "recipient": poetry_agent,
            "message": "Write a poem about it.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
    ]

    arithmetic_agent.register_nested_chats(
        nested_chats,
        # The trigger function is used to determine if the agent should start the nested chat
        # given the sender agent.
        # In this case, the arithmetic agent will not start the nested chats if the sender is
        # from the nested chats' recipient to avoid recursive calls.
        trigger=lambda sender: sender not in [group_chat_manager_with_intros, code_writer_agent, poetry_agent],
    )

    # Instead of using `initiate_chat` method to start another conversation,
    # we can use the `generate_reply` method to get single reply to a message directly.
    reply = arithmetic_agent.generate_reply(
        messages=[{"role": "user", "content": "I have a number 3 and I want to turn it into 7."}]
    )
    ```