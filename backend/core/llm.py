from langchain_openai import ChatOpenAI


def create_llm(model: str, api_key: str) -> ChatOpenAI:
    """Factory for the primary LLM used by the backend graph."""

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0.3,
    )
