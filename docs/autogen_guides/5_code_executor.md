# Code Executor
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
