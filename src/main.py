"""
Elite AI Software Development Team - CLI Entry Point.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from src.crew import create_elite_dev_crew

load_dotenv(ROOT / ".env")


def main() -> None:
    """Run the Elite Dev Crew with user input."""
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if not prompt:
        prompt = input("Enter your software development request: ").strip()
    if not prompt:
        print("No request provided.")
        sys.exit(1)

    if not os.getenv("DEEPSEEK_API_KEY"):
        print(
            "Warning: DEEPSEEK_API_KEY not set. Set it in .env or environment. "
            "Get a key at https://platform.deepseek.com/"
        )

    # Create output directory
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "memory").mkdir(exist_ok=True)

    crew = create_elite_dev_crew()
    print("\n--- Elite AI Software Development Team ---")
    print(f"Request: {prompt}\n")

    result = crew.kickoff(inputs={"topic": prompt})

    print("\n--- Result ---")
    print(result)

    if hasattr(result, "tasks_output"):
        for i, out in enumerate(result.tasks_output, 1):
            print(f"\n--- Task {i} Output ---")
            print(out)


if __name__ == "__main__":
    main()
