# CodePilot AI Architecture

## High-Level Pipeline

User Prompt
↓
Explorer
↓
Planner
↓
Reader
↓
Coder
↓
Executor
↓
Dependency Checker
↓
Build Validator
↓
Runtime Validator
↓
API Tester
↓
Root Cause Analyzer
↓
Reporter

---

## Core Layer

Responsible for repository understanding and code generation.

- Explorer
- Planner
- Reader
- Coder
- Executor
- Summarizer

---

## Verification Layer

Responsible for software verification.

- Dependency Checker
- Build Validator
- Runtime Validator
- API Tester
- Root Cause Analyzer
- Reporter

---

## Services Layer

Shared utilities used across modules.

- Command Runner
- Git Service
- Package Service
- Process Runner