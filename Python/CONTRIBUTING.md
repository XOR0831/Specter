# Contributing to Specter

Thank you for your interest in contributing to **Specter**.

## Project Philosophy

Specter prioritizes correctness, safety, clear architecture, and testability.

## Development Setup

Requirements:
- Python 3.11+
- Poetry

Setup:
```bash
git clone https://github.com/yourusername/specter.git
cd specter
poetry install
```

Run tests:
```bash
poetry run pytest
```

## Guidelines

- All changes must include tests
- Avoid real network calls in tests
- Keep code readable and explicit
- Follow PEP 8

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Ensure tests pass
5. Submit a pull request

## Out of Scope

Specter does not accept exploit payloads, brute-force logic, or malware-related functionality.
