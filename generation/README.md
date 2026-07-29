# CodePilot AI - Generation Engine

The Generation Engine is the core system responsible for transforming
structured engineering plans into production-ready source code.

It consumes the output of the Planning Engine and produces validated,
formatted, and safely written repository changes.

---

# Pipeline Position

The CodePilot AI architecture follows a multi-stage engineering pipeline:

```
User Request
      |
      v
Planning Engine
      |
      v
Generation Engine
      |
      v
Verification Engine
      |
      v
Execution Engine
      |
      v
Reporting Engine
```

The Generation Engine is responsible for the transition:

```
Engineering Plan
        |
        v
Implementation Code
```

---

# Overview

The Generation Engine performs the following operations:

1. Build generation context
2. Optimize repository information
3. Construct LLM prompts
4. Select AI provider
5. Generate source code
6. Parse model responses
7. Validate generated files
8. Format source code
9. Safely write changes

---

# Architecture

High-level flow:

```
GenerationContext

        |
        v

Context Optimizer

        |
        v

Prompt Builder

        |
        v

Provider Layer

        |
        v

LLM Response

        |
        v

Response Parser

        |
        v

Validation Layer

        |
        v

Formatter Layer

        |
        v

Transaction Writer

        |
        v

Repository
```

---

# Package Structure

```
generation/

├── context/
│   Context construction and repository information
│
├── prompt/
│   LLM prompt creation and rendering
│
├── providers/
│   AI provider abstraction layer
│
├── parser/
│   Converts LLM responses into structured models
│
├── formatter/
│   Language-specific source formatting
│
├── writer/
│   Safe repository modification
│
├── services/
│   Generation workflow services
│
├── strategies/
│   Runtime behaviour selection
│
├── generator.py
│   Main generation orchestrator
│
├── explorer.py
│   Repository discovery and analysis
│
├── validator.py
│   Generated code validation
│
├── constants.py
│   Shared immutable configuration
│
├── exceptions.py
│   Generation error hierarchy
│
└── README.md
    Generation documentation
```

---

# Core Components

## 1. Context Layer

Location:

```
generation/context/
```

Responsible for preparing structured information required by the generator.

Main objects:

```
RepositoryContext

ProjectContext

TaskContext

DependencyContext

GenerationContext
```

The complete generation process operates on:

```
GenerationContext
```

instead of passing multiple independent parameters.

---

# 2. Prompt Layer

Location:

```
generation/prompt/
```

Responsible for creating LLM-ready instructions.

Components:

```
PromptBuilder

PromptRenderer

PromptTemplates
```

Flow:

```
GenerationContext

        |
        v

PromptBuilder

        |
        v

Rendered Prompt
```

The prompt layer contains no provider-specific logic.

---

# 3. Provider Layer

Location:

```
generation/providers/
```

Provides a unified interface for different AI models.

Supported providers:

```
OpenAI

Anthropic

Ollama

Mock
```

Architecture:

```
BaseProvider

      |
      +----------------+
      |                |
      v                v

OpenAIProvider   AnthropicProvider

      |
      v

OllamaProvider

      |
      v

MockProvider
```

All providers expose the same interface:

```python
provider.generate(prompt)
```

The generation engine remains independent from the selected AI provider.

---

# 4. Parser Layer

Location:

```
generation/parser/
```

Responsible for converting raw AI responses into structured files.

Flow:

```
LLM Response

      |
      v

CodeBlockParser

      |
      v

MarkdownParser

      |
      v

ResponseParser

      |
      v

CodeResponse
```

Example:

Input:

````markdown
FILE:
src/auth/service.py

```python
def login():
    pass
```