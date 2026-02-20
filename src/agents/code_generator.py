"""Code Generator Agent - Writes production-ready code following the architecture."""

from crewai import Agent

from src.llm import get_llm
from src.tools import read_file_tool, read_directory_tool, retrieve_decisions_tool


def code_generator_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Code Generator Agent",
        goal="Write clean, production-ready code. Follow the architecture exactly. Add comments, typing, and validation. Follow best practices.",
        backstory=(
            "You are an elite software engineer. You implement exactly what the architect "
            "specified. Your code is well-typed, documented, and production-grade. You "
            "never deviate from the defined structure without explicit reason."
        ),
        tools=[read_file_tool, read_directory_tool, retrieve_decisions_tool],
        verbose=True,
        allow_delegation=False,
    )
