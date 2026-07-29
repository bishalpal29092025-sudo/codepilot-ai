# Repository Package

## Responsibility

The Repository package analyses a software repository and extracts
metadata required by CodePilot AI.

It is responsible for:

- Scanning repository files
- Detecting programming language
- Detecting framework
- Detecting database
- Detecting package manager

It is **not** responsible for:

- Code generation
- Repository modification
- LLM interaction
- Command execution

## Public API

```python
from repository import RepositoryExplorer
```

The rest of the implementation is considered internal.

## Future Extensions

- Git analysis
- Docker detection
- CI/CD detection
- Dependency graph generation
- Architecture analysis