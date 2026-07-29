from core.context import AgentContext
from verification.verifier import Verifier


# Create initial agent context
context = AgentContext(
    user_request="Verify demo project"
)


# Create verification engine
verifier = Verifier(
    "./demo-project"
)


# Run complete verification pipeline
context = verifier.verify(
    context
)


# Print final result
print("\nFinal Verification Result:")

print(
    context.verification_result
)