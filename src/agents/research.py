"""Research Agent - Fetches documentation, identifies version changes, provides technical summaries."""

from crewai import Agent

from src.llm import get_llm
from src.tools import read_file_tool, read_directory_tool


def research_agent() -> Agent:
    return Agent(
        llm=get_llm(),
        role="Research Agent",
        goal="Fetch latest official documentation, identify version changes and breaking updates, provide structured technical summaries.",
        backstory=(
            "You are an expert technical researcher. You use Context7, official docs, and "
            "project files to produce accurate, structured summaries. You cite sources and "
            "highlight breaking changes and version differences."
        ),
        tools=[read_file_tool, read_directory_tool],
        verbose=True,
        allow_delegation=False,
    )
