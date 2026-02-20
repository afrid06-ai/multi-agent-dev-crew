"""Architect Agent - Designs scalable, modular architecture, defines structure and APIs."""

from crewai import Agent

from src.llm import get_llm
from src.tools import read_file_tool, retrieve_decisions_tool


def architect_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Architect Agent",
        goal="Design scalable, modular architecture. Define folder structure, APIs, interfaces. Select correct libraries and versions.",
        backstory=(
            "You are a senior software architect. You produce clean architecture docs, "
            "folder layouts, API contracts, and dependency recommendations. You check "
            "past decisions before proposing new ones."
        ),
        tools=[read_file_tool, retrieve_decisions_tool],
        verbose=True,
        allow_delegation=False,
    )
