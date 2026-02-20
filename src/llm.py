"""LLM configuration - DeepSeek (OpenAI-compatible API)."""

import os

from crewai import LLM


def get_llm() -> LLM:
    """Return DeepSeek LLM. Set DEEPSEEK_API_KEY in .env."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY not set. Add it to your .env file. "
            "Get a key at https://platform.deepseek.com/"
        )
    return LLM(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
    )
