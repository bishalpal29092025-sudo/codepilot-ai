from core.context import AgentContext
from verification.dependency_checker import DependencyChecker


# Create context
context = AgentContext(
    user_request="Analyze demo project dependencies"
)


# Create dependency checker
checker = DependencyChecker(
    "./demo-project"
)


# Test repository scan
files = checker._scan_repository()

print("\nDetected Files:")
print(files)


# Run complete detection
context = checker.run(
    context
)


print("\nDependency Report:")
print(context.dependency_report)