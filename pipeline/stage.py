from abc import ABC, abstractmethod

from core.context import AgentContext


class Stage(ABC):
    """
    Base class for every stage in CodePilot AI.
    """

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        self.before(context)

        context = self.execute(context)

        self.after(context)

        return context

    @abstractmethod
    def execute(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Stage implementation.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Stage display name.
        """
        ...

    # ======================================================

    def before(
        self,
        context: AgentContext,
    ) -> None:

        print("\n" + "=" * 80)
        print(f"▶ {self.name}")
        print("=" * 80)

    def after(
        self,
        context: AgentContext,
    ) -> None:

        print(f"✓ {self.name} Complete")