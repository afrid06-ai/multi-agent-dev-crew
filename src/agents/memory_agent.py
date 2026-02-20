"""Memory Agent - Stores decisions, architecture, preferences. Updates memory after tasks."""

from crewai import Agent

from src.llm import get_llm
from src.tools import store_decision_tool, retrieve_decisions_tool


def memory_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Memory Agent",
        goal="Retrieve relevant past project decisions. Store architecture and design decisions. Store user preferences. Update memory after each completed task.",
        backstory=(
            "You are the team's knowledge keeper. You store decisions with correct "
            "categories and tags. You retrieve relevant context for other agents. "
            "You ensure nothing important is lost."
        ),
        tools=[store_decision_tool, retrieve_decisions_tool],
        verbose=True,
        allow_delegation=False,
    )
