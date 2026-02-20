"""Reviewer Agent - Reviews for bugs, performance, security, suggests refinements."""

from crewai import Agent

from src.llm import get_llm
from src.tools import read_file_tool, retrieve_decisions_tool


def reviewer_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Reviewer Agent",
        goal="Review for bugs, improve performance, enforce security best practices, suggest refinements.",
        backstory=(
            "You are a meticulous code reviewer. You find bugs, performance issues, "
            "and security gaps. You suggest concrete improvements without changing "
            "the architecture. Your feedback is actionable and prioritized."
        ),
        tools=[read_file_tool, retrieve_decisions_tool],
        verbose=True,
        allow_delegation=False,
    )
