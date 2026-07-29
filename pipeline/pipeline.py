from core.context import AgentContext

from pipeline.stage import Stage


class Pipeline:
    """
    Executes registered stages in sequence.
    """

    def __init__(
        self,
        stages: list[Stage],
    ):
        self.stages = stages

    def run(
        self,
        context: AgentContext,
    ) -> AgentContext:

        for stage in self.stages:

            context = stage.run(context)

        return context