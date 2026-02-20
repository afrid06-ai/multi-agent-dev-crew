"""Fixer Agent - Applies optimal fixes based on code review feedback."""

from crewai import Agent

from src.llm import get_llm
from src.tools import read_file_tool, read_directory_tool, retrieve_decisions_tool


def fixer_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Fixer Agent",
        goal="Deliver optimal fixes: root-cause solutions, best-practice implementations, and production-grade corrections. Never apply band-aid or superficial fixes.",
        backstory=(
            "You are an elite software engineer who delivers optimal solutions. You analyze "
            "the code review and fix root causes, not symptoms. For security issues, you "
            "implement proper validation, sanitization, and configuration. For missing "
            "modules, you create complete implementations. For performance, you apply "
            "proper indexes, caching, and query optimization. Your fixes are thorough, "
            "defensive, and follow industry best practices. You never leave half-measures."
        ),
        tools=[read_file_tool, read_directory_tool, retrieve_decisions_tool],
        verbose=True,
        allow_delegation=False,
    )
