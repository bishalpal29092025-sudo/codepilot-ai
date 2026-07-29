from core.context import AgentContext
from verification.dependency_checker import DependencyChecker
from verification.build_validator import BuildValidator


context = AgentContext(
    user_request="Build demo project"
)


# Step 1: Detect project
dependency_checker = DependencyChecker(
    "./demo-project"
)

context = dependency_checker.run(
    context
)


# Step 2: Run build validation
validator = BuildValidator(
    "./demo-project"
)

context = validator.run(
    context
)


print("\nBuild Result:")
print(context.build_result)