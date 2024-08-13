# llm_config (https://microsoft.github.io/autogen/docs/topics/llm_configuration)
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