"""
Prompt renderer.

Responsible for rendering prompt templates into
final strings consumed by LLM providers.
"""

from __future__ import annotations

from string import Formatter


class PromptRenderer:
    """
    Renders prompt templates using provided variables.

    This class only handles template rendering.
    """

    def render(
        self,
        template: str,
        **variables: object,
    ) -> str:
        """
        Render a template.

        Args:
            template:
                Prompt template string.

            variables:
                Values used inside the template.

        Returns:
            Rendered prompt string.

        Raises:
            ValueError:
                If required template variables
                are missing.
        """

        required_variables = self._extract_variables(
            template
        )

        missing_variables = [
            variable
            for variable in required_variables
            if variable not in variables
        ]

        if missing_variables:
            raise ValueError(
                "Missing template variables: "
                + ", ".join(missing_variables)
            )

        return template.format(
            **variables
        )

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _extract_variables(
        template: str,
    ) -> list[str]:
        """
        Extract placeholders from template.

        Example:

            "Hello {name}"

        returns:

            ["name"]
        """

        formatter = Formatter()

        variables = []

        for _, field_name, _, _ in formatter.parse(
            template
        ):
            if field_name:
                variables.append(field_name)

        return variables