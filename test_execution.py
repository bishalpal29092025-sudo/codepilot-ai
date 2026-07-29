"""
Execution Engine Test.

Validates:
- Dependency detection
- Environment preparation
- Command execution
- ExecutionResult generation
"""

from core.context import AgentContext

from verification.dependency_checker import DependencyChecker

from execution.executor import Executor


# ==========================================================
# Create Context
# ==========================================================

context = AgentContext(
    user_request="Execute demo project"
)


# ==========================================================
# Dependency Analysis
# ==========================================================

checker = DependencyChecker(
    "./demo-project"
)

context = checker.run(
    context
)


# ==========================================================
# Execute Project
# ==========================================================

executor = Executor(
    "./demo-project"
)


result = executor.execute(
    context,
    [
        "node index.js"
    ],
)


# ==========================================================
# Print Result
# ==========================================================

print("\nExecution Result:")
print(result)