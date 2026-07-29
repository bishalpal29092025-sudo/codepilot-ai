"""
Generation context builder.

Combines repository, project, task, and dependency contexts
into a single immutable GenerationContext.

This is the entry point for building generation input data.
"""

from __future__ import annotations

from core.models.generation import GenerationContext
from core.models.planning import ProjectPlan, Task
from core.models.repository import RepositoryInfo

from .dependency import DependencyContextBuilder
from .project import ProjectContextBuilder
from .repository import RepositoryContextBuilder
from .task import TaskContextBuilder


class GenerationContextBuilder:
    """
    Builds complete GenerationContext objects.

    Responsibilities:
        - Coordinate individual context builders
        - Combine domain contexts
        - Produce immutable generation input

    Does NOT:
        - Generate code
        - Build prompts
        - Call providers
        - Modify repositories
    """

    def __init__(
        self,
        repository_builder: RepositoryContextBuilder | None = None,
        project_builder: ProjectContextBuilder | None = None,
        task_builder: TaskContextBuilder | None = None,
        dependency_builder: DependencyContextBuilder | None = None,
    ) -> None:
        """
        Initialize context builders.
        """

        self.repository_builder = (
            repository_builder
            or RepositoryContextBuilder()
        )

        self.project_builder = (
            project_builder
            or ProjectContextBuilder()
        )

        self.task_builder = (
            task_builder
            or TaskContextBuilder()
        )

        self.dependency_builder = (
            dependency_builder
            or DependencyContextBuilder()
        )

    # =========================================================
    # Public API
    # =========================================================

    def build(
        self,
        *,
        repository: RepositoryInfo,
        project: ProjectPlan,
        task: Task,
        internal_modules: list[str] | None = None,
        external_packages: list[str] | None = None,
        related_files: list[str] | None = None,
        imports: list[str] | None = None,
        dependency_graph: dict[str, list[str]] | None = None,
    ) -> GenerationContext:
        """
        Build complete GenerationContext.

        Args:
            repository:
                Repository metadata.

            project:
                Planning output.

            task:
                Current implementation task.

            dependency information:
                Dependency information required
                for generation.

        Returns:
            Immutable GenerationContext.
        """

        return GenerationContext(
            repository=self.repository_builder.build(
                repository
            ),
            project=self.project_builder.build(
                project
            ),
            task=self.task_builder.build(
                task
            ),
            dependencies=self.dependency_builder.build(
                internal_modules=internal_modules,
                external_packages=external_packages,
                related_files=related_files,
                imports=imports,
                dependency_graph=dependency_graph,
            ),
        )