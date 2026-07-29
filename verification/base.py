from abc import ABC, abstractmethod

from core.context import AgentContext


class VerificationStage(ABC):
    """
    Base class for all verification stages.

    Every verification module should inherit from this class.
    """

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        self.print_header()

        context = self.execute(context)

        self.print_summary(context)

        return context

    @abstractmethod
    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Execute verification logic.

        Must be implemented by subclasses.
        """
        ...

    @abstractmethod
    def stage_name(self) -> str:
        """
        Display name of the stage.
        """
        ...

    # ==========================================================
    # Helpers
    # ==========================================================

    def extract_errors(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        return [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

    # ==========================================================
    # Console
    # ==========================================================

    def print_header(self) -> None:

        print("\n" + "=" * 70)
        print(f"🔍 {self.stage_name()}")
        print("=" * 70)

    def print_summary(
        self,
        context: AgentContext,
    ) -> None:

        print("Completed.")