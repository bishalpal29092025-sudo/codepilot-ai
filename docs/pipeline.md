# Agent Pipeline

Explorer
↓

Planner
↓

Reader
↓

Coder
↓

Executor
↓

Verification

↓

Reporter

All modules communicate using AgentContext.

Each module implements:

run(context) -> AgentContext