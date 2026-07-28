# 🚀 CodePilot AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI%20SDK-Compatible-412991?style=for-the-badge)
![Cerebras](https://img.shields.io/badge/LLM-Cerebras-gpt--oss--120b-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### An AI Coding Agent that understands repositories, plans implementations, generates production-ready code, and automatically applies changes.

---

**Repository Analysis • Planning • Context Reading • Code Generation • File Writing • Implementation Summary**

</div>

---

# 📖 Overview

CodePilot AI is an intelligent coding assistant built to automate software development tasks by understanding an existing codebase before generating code.

Unlike a simple code generator, CodePilot AI first explores the repository, detects the project's technology stack, identifies the files required for the requested feature, reads the relevant context, generates implementation code using an LLM, applies the modifications, and finally summarizes the completed work.

The project demonstrates how modern AI coding agents work internally by combining repository analysis, structured planning, contextual reasoning, and automated code generation into a complete development workflow.

---

# ✨ Features

## 🔍 Repository Analysis

- Automatically scans an entire repository
- Detects project language
- Detects framework
- Detects database
- Detects package manager
- Builds repository context

Supported technologies include:

- JavaScript
- TypeScript
- Python
- Express.js
- Next.js
- React
- MongoDB
- PostgreSQL
- MySQL

---

## 🧠 Intelligent Planning

Instead of immediately generating code, the agent first creates an implementation plan.

The planner determines:

- Goal
- Required files
- Implementation steps
- Potential risks
- Testing recommendations

This planning step significantly improves code quality by giving the model additional reasoning before generation.

---

## 📖 Context-Aware Reading

Only the files required for the implementation are loaded.

Features include:

- Missing file detection
- Binary file detection
- UTF-8 validation
- File size limits
- Repository context formatting

This allows the LLM to understand the existing architecture before modifying it.

---

## 💻 AI Code Generation

CodePilot AI uses the **GPT OSS 120B** model running on the **Cerebras Inference API**.

The generated output is structured as JSON and includes:

- Modified files
- Newly created files
- Complete source code

This structured approach makes it easier to validate and apply changes safely.

---

## 📝 Automatic File Writing

Generated code is automatically written back into the target repository.

Capabilities include:

- Creating new files
- Updating existing files
- Creating missing directories
- Preventing invalid file paths

---

## 📋 Implementation Summary

After applying changes, the agent generates a structured implementation summary containing:

- Modified files
- Added features
- Testing recommendations
- Developer notes

---

# 🎯 Objectives

The primary goals of CodePilot AI are:

- Understand an existing codebase
- Plan feature implementation
- Read only relevant project files
- Generate context-aware code
- Apply changes automatically
- Produce implementation summaries
- Demonstrate an end-to-end AI software engineering workflow

---

# 🏗️ High-Level Architecture

```text
                    User Request
                          │
                          ▼
                  Repository Explorer
                          │
                          ▼
                    Project Planner
                          │
                          ▼
                 Repository Reader
                          │
                          ▼
                  Code Generator (LLM)
                          │
                          ▼
                    Code Executor
                          │
                          ▼
                    Summary Generator
```

---

# ⚙️ System Workflow

```text
User
 │
 ▼
Describe the feature
 │
 ▼
Repository Analysis
 │
 ▼
Technology Detection
 │
 ▼
Implementation Planning
 │
 ▼
Read Required Files
 │
 ▼
Generate Code
 │
 ▼
Apply Changes
 │
 ▼
Generate Summary
 │
 ▼
Completed
```

---

# 🎬 Demonstration

Example user request:

```text
Add JWT authentication using Express middleware.
```

The agent automatically:

1. Analyses the repository.
2. Detects the Express.js framework.
3. Identifies relevant source files.
4. Reads the project context.
5. Generates authentication code.
6. Creates missing files.
7. Updates existing routes.
8. Writes the generated code.
9. Produces a summary of all modifications.

The generated application was successfully started after installing the required dependencies, demonstrating an end-to-end AI-assisted development workflow.

---

# 📸 Screenshots

> Add screenshots of:

- Repository analysis
- Planner output
- Repository reader
- Code generation
- Code execution
- Summary output
- Running application

Example:

```
docs/
├── repository-analysis.png
├── planner.png
├── reader.png
├── generator.png
├── executor.png
└── summary.png
```

---

# 📁 Project Structure

```text
codepilot-ai/
│
├── agent.py                  # Main entry point
├── config.py                 # Environment configuration
├── llm.py                    # Cerebras/OpenAI wrapper
├── requirements.txt
├── .env.example
├── README.md
│
├── core/
│   ├── models.py             # Pydantic models
│   ├── explorer.py           # Repository scanner
│   ├── planner.py            # Feature planning
│   ├── reader.py             # Repository context reader
│   ├── coder.py              # AI code generation
│   ├── executor.py           # Applies generated code
│   └── summarizer.py         # Implementation summary
│
├── prompts/
│   ├── planner.txt
│   ├── coder.txt
│   └── summary.txt
│
└── notes-app/                # Demo repository (example target project)
```

---

# 🏛️ Project Architecture

```text
                  ┌──────────────────────┐
                  │       User           │
                  └──────────┬───────────┘
                             │
                             ▼
                    Feature Request
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Repository Explorer  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Planner          │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Repository Reader    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ GPT OSS 120B (LLM)   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Code Generator       │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Code Executor        │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Summary Generator    │
                  └──────────────────────┘
```

---

# 🛠️ Tech Stack

## Programming Language

- Python 3.10+

---

## AI Model

- GPT OSS 120B

---

## Inference Provider

- Cerebras AI

---

## SDK

- OpenAI Python SDK (compatible with Cerebras API)

---

## Data Validation

- Pydantic

---

## Environment Management

- python-dotenv

---

## Prompt Engineering

- External Prompt Templates

---

## Target Repositories

Supports repositories built with:

- JavaScript
- TypeScript
- Python

Framework detection:

- Express.js
- Next.js
- React
- Flask
- Django
- FastAPI

Databases:

- MongoDB
- PostgreSQL
- MySQL

---

# ⚙️ Requirements

- Python 3.10 or newer
- Cerebras API Key
- Internet connection
- A target repository to analyse

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/codepilot-ai.git

cd codepilot-ai
```

---

## Create a Virtual Environment

macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
CEREBRAS_API_KEY=your_api_key_here

MODEL=gpt-oss-120b

BASE_URL=https://api.cerebras.ai/v1

DEFAULT_REPOSITORY=../notes-app
```

---

# 📂 Configuration

The project uses `config.py` to load environment variables.

Current configuration:

```python
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

MODEL = "gpt-oss-120b"

BASE_URL = "https://api.cerebras.ai/v1"

DEFAULT_REPOSITORY = "../notes-app"
```

To analyse another repository, simply update:

```python
DEFAULT_REPOSITORY = "../your-project"
```

or modify the configuration to accept the repository path from the command line.

---

# 📦 Python Dependencies

Example `requirements.txt`

```text
openai
python-dotenv
pydantic
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📂 Target Repository

CodePilot AI does **not** modify itself.

Instead, it analyses and updates a separate project.

Example:

```text
AI-Coding-Agent/
│
├── codepilot-ai/
│
└── notes-app/
```

In this project, **notes-app** is a demonstration repository used to validate the agent.

Any compatible repository can be analysed by changing the `DEFAULT_REPOSITORY` path.

---

# 🚦 Quick Start

Run the agent:

```bash
python agent.py
```

Example prompt:

```text
Add JWT authentication using Express middleware.
```

The agent will:

- Analyse the repository
- Plan the implementation
- Read relevant files
- Generate code
- Apply changes
- Produce a structured implementation summary

---

# ▶️ Usage

Once the environment is configured and the dependencies are installed, start the AI coding agent by running:

```bash
python agent.py
```

The application will prompt you to describe the feature you want to implement.

Example:

```text
Describe what you'd like to implement:

> Add JWT authentication using Express middleware.
```

---

# 🔄 End-to-End Workflow

The complete workflow executed by CodePilot AI is shown below.

```text
                     User
                      │
                      ▼
          Describe a new feature
                      │
                      ▼
           Repository Explorer
                      │
                      ▼
        Detect Project Information
                      │
                      ▼
        Framework Detection
                      │
                      ▼
        Database Detection
                      │
                      ▼
         Package Manager Detection
                      │
                      ▼
               Planner (LLM)
                      │
                      ▼
         Repository Reader
                      │
                      ▼
      Load Relevant Project Files
                      │
                      ▼
           Code Generator (LLM)
                      │
                      ▼
            JSON Code Response
                      │
                      ▼
             Code Executor
                      │
                      ▼
         Updated Repository Files
                      │
                      ▼
            Summary Generator
                      │
                      ▼
             Final Report
```

---

# 🧠 AI Pipeline

The agent follows a structured reasoning pipeline instead of directly generating code.

## Step 1 — Repository Analysis

The Repository Explorer scans the entire repository and collects metadata including:

- Programming language
- Framework
- Database
- Package manager
- Important project files

Example:

```text
Repository Analysis

Language          : JavaScript
Framework         : Express.js
Database          : MongoDB
Package Manager   : npm

Total Files : 11
```

---

## Step 2 — Planning

The planner receives:

- User request
- Repository metadata

It generates a structured implementation plan containing:

- Goal
- Relevant files
- Implementation steps
- Risks
- Testing recommendations

Example:

```text
Goal

Implement JWT Authentication.

Relevant Files

src/app.js

src/routes/auth.routes.js

src/controllers/auth.controller.js

src/middleware/auth.middleware.js
```

---

## Step 3 — Repository Reader

The Repository Reader loads only the files required by the planner.

Features:

- Missing file detection
- Binary file detection
- UTF-8 validation
- Maximum file size protection

Example:

```text
Loaded : 6

Missing : 3

Skipped : 0
```

---

## Step 4 — AI Code Generation

The loaded repository context is sent to GPT OSS 120B running on Cerebras.

The model returns structured JSON describing:

- Updated files
- Newly created files
- Source code

Example:

```json
{
    "files":[
        {
            "path":"src/routes/auth.routes.js",
            "content":"..."
        }
    ]
}
```

---

## Step 5 — Code Execution

Generated files are automatically written back into the repository.

Capabilities include:

- Updating files
- Creating files
- Creating directories
- Safe path validation

Example:

```text
Written : 6

Failed : 0
```

---

## Step 6 — Implementation Summary

Finally, the summarizer produces a structured report including:

- Modified files
- New features
- Testing recommendations
- Developer notes

Example:

```text
Files Changed

✓ src/app.js

✓ src/routes/auth.routes.js

✓ src/controllers/auth.controller.js

Features

• JWT Authentication

• Login endpoint

• Registration endpoint

• Authentication middleware

Testing

• Verify login

• Verify protected routes

• Test invalid token

Notes

• Configure JWT_SECRET
```

---

# 📊 Example Console Output

```text
🚀 CodePilot AI

Repository Analysis

Language : JavaScript

Framework : Express.js

Planner

Repository Reader

Loaded : 6

Missing : 3

Code Generator

Generated : 6 Files

Executor

Written : 6 Files

Summary

Completed
```

---

# 🧪 Validation

The generated implementation was validated by running the modified application.

Validation steps:

1. Install generated dependencies.

```bash
npm install
```

2. Start the application.

```bash
npm run dev
```

Successful output:

```text
MongoDB Connected Successfully

Server running on http://localhost:5001
```

This demonstrates that the generated code integrates successfully with the existing repository.

---

# 📸 Screenshots

Recommended screenshots for the repository.

```
docs/

├── 01-repository-analysis.png

├── 02-planner.png

├── 03-reader.png

├── 04-generator.png

├── 05-executor.png

├── 06-summary.png

└── 07-running-server.png
```

Example:

## Repository Analysis

> *(Insert screenshot here)*

---

## Planner

> *(Insert screenshot here)*

---

## Repository Reader

> *(Insert screenshot here)*

---

## Code Generation

> *(Insert screenshot here)*

---

## Code Execution

> *(Insert screenshot here)*

---

## Final Summary

> *(Insert screenshot here)*

---

## Running Application

> *(Insert screenshot here)*

---

# 📈 Example Development Scenario

### User Request

```text
Add JWT authentication using Express middleware.
```

### Repository Analysis

- Express.js
- MongoDB
- npm

### Planner

Determines:

- Required files
- Missing files
- Authentication strategy

### Reader

Loads only the required files.

### Generator

Creates:

- auth.controller.js
- auth.routes.js
- auth.middleware.js
- user.model.js

Updates:

- app.js
- note.routes.js

### Executor

Writes generated files to the repository.

### Summarizer

Produces a structured report describing the completed implementation.

---

# 🧩 Core Components

CodePilot AI is built using a modular architecture where every component has a single responsibility.

---

## Repository Explorer

**Location**

```text
core/explorer.py
```

### Responsibilities

- Scan the repository recursively
- Detect programming language
- Detect framework
- Detect package manager
- Detect database
- Collect important project files
- Build repository metadata

### Output

```python
RepositoryContext(
    language="JavaScript",
    framework="Express.js",
    database="MongoDB",
    package_manager="npm",
    files=[...]
)
```

---

## Planner

**Location**

```text
core/planner.py
```

The planner converts a natural language request into a structured implementation plan.

Example request:

```text
Add JWT Authentication
```

Example output:

```json
{
  "goal": "...",
  "relevant_files": [],
  "implementation_steps": [],
  "risks": [],
  "testing": []
}
```

Using a planning phase before generation significantly improves the quality and consistency of generated code.

---

## Repository Reader

**Location**

```text
core/reader.py
```

Instead of loading the entire repository into the model context, only the files selected by the planner are read.

### Features

- UTF-8 validation
- Binary file detection
- Missing file detection
- File size limits
- Repository context formatting

This reduces token usage while providing the model with the information needed for accurate code generation.

---

## Code Generator

**Location**

```text
core/coder.py
```

The Code Generator combines:

- User request
- Implementation plan
- Repository context

and sends them to the LLM.

Expected output:

```json
{
  "files":[
    {
      "path":"src/app.js",
      "content":"..."
    }
  ]
}
```

Returning structured JSON makes it easier to validate and safely apply generated changes.

---

## Code Executor

**Location**

```text
core/executor.py
```

Responsibilities:

- Create missing directories
- Create new files
- Update existing files
- Validate paths
- Prevent invalid writes

Example:

```text
Writing...

✓ src/app.js

✓ src/routes/auth.routes.js

✓ src/controllers/auth.controller.js
```

---

## Summary Generator

**Location**

```text
core/summarizer.py
```

The final step generates a concise report describing:

- Files modified
- Features implemented
- Testing suggestions
- Additional notes

This gives developers a quick overview of what changed.

---

# 🤖 LLM Integration

CodePilot AI uses the GPT OSS 120B model served through the Cerebras Inference API.

The project communicates using the OpenAI-compatible SDK.

Example:

```python
client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ],
)
```

---

# 📝 Prompt Engineering

The prompts are stored separately from the application logic.

```text
prompts/

planner.txt

coder.txt

summary.txt
```

Separating prompts from code provides several advantages:

- Easier prompt iteration
- Cleaner architecture
- Better maintainability
- Reduced coupling between business logic and prompt design

---

## Planner Prompt

Responsible for producing a structured implementation plan.

Returns:

```json
{
  "goal": "",
  "relevant_files": [],
  "implementation_steps": [],
  "risks": [],
  "testing": []
}
```

---

## Code Generation Prompt

Receives:

- User request
- Repository context
- Implementation plan

Returns:

```json
{
  "files":[]
}
```

---

## Summary Prompt

Produces a developer-friendly implementation report.

Returns:

```json
{
  "files_changed": [],
  "features_added": [],
  "testing": [],
  "notes": []
}
```

---

# 📦 Data Models

The project uses **Pydantic** to validate every LLM response before processing.

Models include:

```text
Plan

RepositoryContext

GeneratedFile

CodeResponse

ExecutionResult

Summary
```

Using typed models helps detect malformed responses before they affect the repository.

---

# ⚠️ Error Handling

The application includes defensive checks throughout the pipeline.

Examples include:

- Missing API key
- Invalid JSON from the model
- Empty model responses
- Missing repository files
- Invalid paths
- UTF-8 decoding errors
- File writing failures

Rather than silently failing, meaningful error messages are displayed to assist debugging.

---

# 🔒 Safety Considerations

To reduce the risk of unintended changes, the executor validates file paths before writing.

Current safeguards include:

- Preventing invalid paths
- Restricting writes to the target repository
- Creating directories only when required

Additional safeguards such as approval workflows and patch previews are planned for future versions.

---

# 🧪 Testing Strategy

The project was validated using a real Express.js application (`notes-app`) as the target repository.

Validation process:

1. Analyse repository
2. Generate implementation plan
3. Read project context
4. Generate authentication feature
5. Apply generated code
6. Install dependencies
7. Start application

Successful execution confirmed that the generated implementation integrated correctly with the existing project.

---

# 💡 Design Decisions

Several architectural decisions were made while building CodePilot AI.

### Why plan before generating?

Planning allows the model to identify the relevant files and implementation strategy before writing code, improving consistency.

---

### Why load only relevant files?

Loading only the required context reduces token usage and helps the model focus on the implementation.

---

### Why use structured JSON?

Structured outputs are easier to validate, safer to process, and simpler to apply than free-form text.

---

### Why separate prompts?

Prompt engineering evolves independently of application logic. Keeping prompts in dedicated files improves maintainability.

---

### Why modular architecture?

Each component performs one responsibility, making the project easier to extend, test, and debug.

---

# 📊 Performance Considerations

Current optimisations include:

- Reading only relevant files
- External prompt templates
- Structured JSON responses
- Typed validation
- Modular pipeline

These choices improve maintainability while reducing unnecessary model context.

---

# ⚠️ Current Limitations

While CodePilot AI demonstrates a complete AI-assisted software engineering workflow, the current version has a few limitations.

## Dependency Management

The agent can generate code that imports new libraries but does **not automatically update dependency files** such as:

- `package.json`
- `requirements.txt`
- `Cargo.toml`
- `go.mod`

Developers must install any newly required packages manually.

Example:

```bash
npm install jsonwebtoken bcrypt
```

---

## No Automatic Testing

The generated code is written directly to the repository.

The agent does not currently:

- Execute unit tests
- Run integration tests
- Verify build success automatically

Testing remains the responsibility of the developer.

---

## Limited Language Detection

The current repository analyser focuses primarily on:

- JavaScript
- TypeScript
- Python

Support for additional ecosystems can be added in future releases.

---

## Single-Agent Architecture

The current implementation uses a single AI agent that performs planning and code generation sequentially.

Future versions may introduce specialised agents for planning, coding, testing, reviewing, and documentation.

---

# 🚀 Roadmap

The following features are planned for future versions of CodePilot AI.

## Version 2

- Multi-agent architecture
- Automatic dependency management
- Git diff generation
- Interactive approval before writing files
- Streaming LLM responses
- Improved repository understanding

---

## Version 3

- Unit test generation
- Automatic test execution
- Bug fixing mode
- Refactoring mode
- Code review mode
- Documentation generation

---

## Long-Term Vision

The long-term goal is to build an AI software engineering assistant capable of:

- Understanding large repositories
- Planning complex features
- Writing production-ready code
- Running automated tests
- Fixing bugs
- Reviewing pull requests
- Generating documentation
- Assisting developers throughout the software development lifecycle

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve CodePilot AI:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/new-feature
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature/new-feature
```

5. Open a Pull Request.

Please ensure that new code follows the existing project structure and includes clear documentation where appropriate.

---

# 📚 References

This project was inspired by recent advances in AI-assisted software engineering and large language models.

Relevant technologies include:

- OpenAI-compatible APIs
- Cerebras Inference API
- Pydantic
- Python
- Repository-aware AI agents
- Prompt engineering
- Structured JSON outputs

---

# 🛡️ License

This project is licensed under the **MIT License**.

You are free to:

- Use
- Modify
- Distribute
- Fork

provided that the original license is included.

---

# 🙏 Acknowledgements

Special thanks to the open-source community and the teams building modern AI tooling.

This project makes use of:

- Python
- OpenAI-compatible SDK
- Cerebras Inference API
- Pydantic
- python-dotenv

Their tools and documentation made this project possible.

---

# 👨‍💻 Author

**Bishal Pal**

MCA Student • Full-Stack Developer • AI Enthusiast

### Areas of Interest

- Artificial Intelligence
- Large Language Models (LLMs)
- AI Agents
- Full-Stack Development
- Backend Engineering
- DevOps
- Machine Learning

---

# 🌟 Support

If you found this project helpful:

- ⭐ Star the repository
- 🍴 Fork the repository
- 🐛 Report issues
- 💡 Suggest improvements
- 🤝 Contribute new features

Community contributions are always appreciated.

---

# 📌 Project Status

**Current Status:** Active Development

The project has successfully demonstrated:

- ✅ Repository analysis
- ✅ Intelligent planning
- ✅ Context-aware file reading
- ✅ AI-powered code generation
- ✅ Automatic file writing
- ✅ Structured implementation summaries

Future development will focus on expanding automation, safety, testing, and support for additional programming languages and frameworks.

---

# 📄 Citation

If you use CodePilot AI in your work, presentations, or research, please consider referencing the project.

```text
Bishal Pal.
CodePilot AI: A Repository-Aware AI Coding Agent.
GitHub Repository.
```

---

# ⭐ Final Thoughts

CodePilot AI demonstrates how modern AI systems can move beyond simple code completion to perform structured software engineering tasks.

By combining repository analysis, planning, contextual understanding, AI-powered code generation, and automated code application, the project showcases an end-to-end development workflow inspired by the next generation of AI coding assistants.

The project is designed as both a practical development tool and a learning resource for understanding how repository-aware AI agents can be built using Python, structured prompts, and large language models.

---

<div align="center">

## ⭐ If you enjoyed this project, consider giving it a Star!

**Happy Coding! 🚀**

Made with ❤️ using Python, Cerebras, and GPT OSS 120B.

</div>