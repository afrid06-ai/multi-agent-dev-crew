"""
Dry run of the Elite Dev Team - produces sample output without calling LLMs.
Use this for reference when the full crew cannot be executed.
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent

SAMPLE_OUTPUT = """
================================================================================
ELITE AI SOFTWARE DEVELOPMENT TEAM - SAMPLE OUTPUT
================================================================================
Request: Create a Python function that calculates factorial

--------------------------------------------------------------------------------
TASK 1 - RESEARCH AGENT OUTPUT
--------------------------------------------------------------------------------

# Technical Summary: Python Factorial Implementation

## Documentation References
- Python 3.x math.factorial exists for non-negative integers
- For educational/custom implementation: recursive or iterative approach
- No breaking changes in recent Python versions for basic math operations

## Recommendations
- Use `int` type hints
- Handle edge cases: n=0 (returns 1), n<0 (raise ValueError)
- Consider `math.factorial` vs custom for production

--------------------------------------------------------------------------------
TASK 2 - ARCHITECT AGENT OUTPUT
--------------------------------------------------------------------------------

# Architecture: Factorial Module

## Structure
```
project/
  factorial.py    # Main implementation
  test_factorial.py  # Unit tests (optional)
```

## API
- `factorial(n: int) -> int` - Compute n!
- Raises: ValueError if n < 0
- Returns: 1 for n=0

## Dependencies
- Python 3.8+ (typing)
- No external libraries required

--------------------------------------------------------------------------------
TASK 3 - CODE GENERATOR AGENT OUTPUT
--------------------------------------------------------------------------------

# implementation.md

```python
def factorial(n: int) -> int:
    \"\"\"
    Compute the factorial of a non-negative integer.
    
    Args:
        n: Non-negative integer
        
    Returns:
        n! (n factorial)
        
    Raises:
        ValueError: If n is negative
    \"\"\"
    if n < 0:
        raise ValueError("factorial() not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

--------------------------------------------------------------------------------
TASK 4 - REVIEWER AGENT OUTPUT
--------------------------------------------------------------------------------

# Code Review Report

## Summary: APPROVED with minor suggestions

## Bugs Found
- None critical. Implementation is correct.

## Performance
- Iterative approach avoids stack overflow for large n.
- Consider documenting max practical n (Python int is unlimited, but time grows).

## Security
- Input validation (n < 0) is present. Good.
- Consider type checking for non-integer input (float, str) - may raise naturally.

## Refinements
1. Add docstring examples: `>>> factorial(5)` -> 120
2. Optional: Add `@lru_cache` for repeated small n if needed

--------------------------------------------------------------------------------
TASK 5 - MEMORY AGENT OUTPUT
--------------------------------------------------------------------------------

## Stored Decisions

1. **architecture** - Factorial implemented as standalone function in factorial.py
2. **library** - No external dependencies; stdlib only
3. **preference** - Iterative over recursive for stack safety

Memory updated successfully. 3 decisions stored.
"""


def main():
    (ROOT / "output").mkdir(exist_ok=True)
    out_path = ROOT / "output" / "dry_run_sample_output.txt"
    out_path.write_text(SAMPLE_OUTPUT, encoding="utf-8")
    print(SAMPLE_OUTPUT)
    print(f"\n[Sample output also saved to {out_path}]")


if __name__ == "__main__":
    main()
