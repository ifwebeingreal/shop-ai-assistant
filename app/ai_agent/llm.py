from langchain_ollama import ChatOllama

from config import config


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=config.agent.model,
        temperature=config.agent.temperature,
        base_url=config.agent.ollama_base_url,
        num_predict=256,
        num_ctx=4096,
        client_kwargs={"timeout": 120.0},
    )