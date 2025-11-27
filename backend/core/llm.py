from langchain_openai import ChatOpenAI

from backend.core.config import settings


def create_llm(model: str = "gpt-4o-mini") -> ChatOpenAI:
    """Factory for the primary LLM used by the backend graph."""

    return ChatOpenAI(
        model=model,
        api_key=settings.openai_api_key,
        temperature=0.3,
    )
