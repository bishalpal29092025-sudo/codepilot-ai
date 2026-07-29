"""
Prompt templates used by the Generation package.

Templates define the structure of prompts sent to
LLM providers.
"""


SYSTEM_TEMPLATE = """
You are CodePilot AI, an expert software engineering agent.

Your responsibility is to generate production-quality code.

Follow these rules:

- Respect existing architecture.
- Do not introduce unnecessary dependencies.
- Follow project coding standards.
- Produce clean, maintainable code.
- Explain important decisions when required.
"""


REPOSITORY_TEMPLATE = """
Repository Information:

Name:
{repository_name}

Language:
{language}

Frameworks:
{frameworks}

Files:
{repository_files}
"""


PROJECT_TEMPLATE = """
Project Information:

Name:
{project_name}

Summary:
{summary}

Objective:
{objective}

Architecture:
{architecture}

Constraints:
{constraints}

Coding Standards:
{coding_standards}
"""


TASK_TEMPLATE = """
Implementation Task:

Title:
{task_title}

Description:
{task_description}

Priority:
{priority}

Complexity:
{complexity}

Acceptance Criteria:
{acceptance_criteria}

Relevant Files:
{relevant_files}
"""


DEPENDENCY_TEMPLATE = """
Dependencies:

Internal Modules:
{internal_modules}

External Packages:
{external_packages}

Required Imports:
{imports}
"""


CODE_GENERATION_TEMPLATE = """
Generate the required code changes.

Return only the necessary files.

For every file provide:

FILE:
<relative path>

CODE:
<complete file content>

Task:
{task}
"""