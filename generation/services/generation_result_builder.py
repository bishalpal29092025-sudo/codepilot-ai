"""
Generation result builder.

Creates structured generation results from
generated code responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from core.models.generation import CodeResponse


class GenerationResultBuilder:
    """
    Builds generation execution results.
    """

    def build(
        self,
        response: CodeResponse,
        *,
        provider: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build generation result.

        Args:
            response:
                Parsed generated code response.

            provider:
                Provider used for generation.

            metadata:
                Additional information.

        Returns:
            Structured generation result.
        """

        return {
            "provider": provider,
            "files_generated": len(
                response.files
            ),
            "files": [
                {
                    "path": file.path,
                    "content": file.content,
                }
                for file in response.files
            ],
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }