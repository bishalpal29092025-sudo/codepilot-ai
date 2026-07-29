from dataclasses import dataclass
from typing import Optional

from core.models import (
    Plan,
    RepositoryContext,
    CodeResponse,
    ExecutionResult,
    Summary,
)


@dataclass
class AgentContext:
    user_request: str

    repository_info: Optional[dict] = None

    plan: Optional[Plan] = None

    repository_context: Optional[RepositoryContext] = None

    generated_code: Optional[CodeResponse] = None

    execution_result: Optional[ExecutionResult] = None

    summary: Optional[Summary] = None