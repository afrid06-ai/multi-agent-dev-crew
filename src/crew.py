"""
Elite AI Software Development Team - CrewAI Crew.
Sequential workflow: Research → Architect → Code Generator → Reviewer → [Fixer → Reviewer]×2 → Memory.
"""

from crewai import Crew, Process, Task

from src.agents import (
    research_agent,
    architect_agent,
    code_generator_agent,
    reviewer_agent,
    fixer_agent,
    memory_agent,
)


def create_research_task() -> Task:
    return Task(
        description=(
            "Research the user's request: {topic}. Fetch latest documentation if relevant. "
            "Identify version changes, breaking updates. Produce a structured technical summary. "
            "Use read_file_tool and read_directory_tool to explore the project. "
            "Output: Markdown document with findings, sources, and recommendations."
        ),
        expected_output="Structured technical summary in Markdown with findings, version info, and documentation links.",
        agent=research_agent(),
    )


def create_architect_task(research_task: Task) -> Task:
    return Task(
        description=(
            "Design the architecture for: {topic}. Base it on the research output. Define folder structure, "
            "APIs, interfaces. Select libraries and versions. Check past decisions with "
            "retrieve_decisions_tool before proposing. Output a clear architecture document."
        ),
        expected_output="Architecture document: folder structure, API definitions, library choices, interface contracts.",
        agent=architect_agent(),
        context=[research_task],
    )


def create_code_task(architect_task: Task) -> Task:
    return Task(
        description=(
            "Implement the software for: {topic}. Follow the architecture exactly. Write production-ready "
            "code with typing, comments, validation. Use read_file_tool to reference specs. "
            "Create all necessary files. Follow best practices."
        ),
        expected_output="Complete, working code files. Well-typed, documented, production-grade implementation.",
        agent=code_generator_agent(),
        context=[architect_task],
        output_file="output/implementation.md",
    )


def create_review_task(code_task: Task) -> Task:
    return Task(
        description=(
            "Review the generated code. Check for bugs, performance issues, security gaps. "
            "Provide actionable feedback and suggest refinements. Prioritize critical issues."
        ),
        expected_output="Code review report: bugs found, performance suggestions, security notes, refinement recommendations.",
        agent=reviewer_agent(),
        context=[code_task],
        output_file="output/review_report.md",
    )


def create_fix_task(code_task: Task, review_task: Task) -> Task:
    return Task(
        description=(
            "Apply OPTIMAL fixes based on the code review. For each issue, provide the best "
            "solution—fix root causes, not symptoms. For security: proper env-based config, "
            "input validation, SQL injection protection. For missing modules: full, correct "
            "implementations. For performance: indexes, connection pooling, proper queries. "
            "Never use placeholders or TODO comments—deliver complete, production-ready code. "
            "Use read_file_tool to read output/implementation.md and output/review_report.md. "
            "Preserve the architecture. Output the complete corrected implementation."
        ),
        expected_output="Optimal, complete implementation with all issues properly fixed. Production-ready, no placeholders.",
        agent=fixer_agent(),
        context=[code_task, review_task],
        output_file="output/implementation.md",
    )


def create_memory_task(research_task: Task, architect_task: Task, review_task: Task) -> Task:
    return Task(
        description=(
            "Store key decisions from this session. Use store_decision_tool to save: "
            "1) Architecture choices, 2) Library selections, 3) User preferences from the request. "
            "Use retrieve_decisions_tool to avoid duplicates. Summarize what was stored."
        ),
        expected_output="Summary of stored decisions. Confirmation that memory was updated.",
        agent=memory_agent(),
        context=[research_task, architect_task, review_task],
    )


def create_elite_dev_crew() -> Crew:
    """Create the Elite AI Software Development Team crew with review-fix loop (2 cycles)."""
    t1 = create_research_task()
    t2 = create_architect_task(t1)
    t3 = create_code_task(t2)
    t4 = create_review_task(t3)
    # Fix cycle 1
    t5 = create_fix_task(t3, t4)
    t6 = create_review_task(t5)
    # Fix cycle 2
    t7 = create_fix_task(t5, t6)
    t8 = create_review_task(t7)
    # Memory uses final review
    t9 = create_memory_task(t1, t2, t8)

    return Crew(
        agents=[
            research_agent(),
            architect_agent(),
            code_generator_agent(),
            reviewer_agent(),
            fixer_agent(),
            memory_agent(),
        ],
        tasks=[t1, t2, t3, t4, t5, t6, t7, t8, t9],
        process=Process.sequential,
        verbose=True,
    )
