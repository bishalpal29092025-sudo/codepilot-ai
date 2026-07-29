from agent.agent import CodePilotAgent


agent = CodePilotAgent(
    "./demo-project"
)


context = agent.run(
    """
Analyze this project.

Check the implementation,
identify possible improvements,
generate required changes,
execute validation,
and create a final engineering report.
"""
)


print("\n")
print("=" * 70)
print("FINAL ENGINEERING REPORT")
print("=" * 70)


print(
    context.engineering_report
)