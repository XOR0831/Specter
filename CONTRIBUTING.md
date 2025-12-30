# Contributing to Specter

Thanks for your interest in contributing to **Specter**!  
This project is a long-term, multi-language exploration of networking and systems engineering.

We welcome contributions of all kinds — code, documentation, tests, ideas, and discussions.

---

## 📌 Project Scope

Specter is implemented in **multiple languages**, each treated as a first-class citizen:

- **Python** – reference implementation, feature-complete
- **Go** – concurrency-focused implementation
- **Rust** – safety and performance-focused implementation

Each language lives in its own directory and follows its ecosystem’s best practices.

---

## 🧭 How to Contribute

### 1. Pick an Area

You can contribute by:
- Implementing missing features in Go or Rust
- Improving performance or correctness
- Adding tests or benchmarks
- Improving documentation
- Fixing bugs or refactoring code
- Improving CI, security, or release automation

---

### 2. Fork & Branch

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feat/my-feature
   ```

---

### 3. Follow Commit Conventions

This project enforces **Conventional Commits**.

Examples:
```
feat: add UDP scanning support
fix: handle socket timeout correctly
docs: improve root README
refactor: simplify TCP scanner
test: add banner grabbing tests
ci: add lint stage to pipeline
```

---

### 4. Language-Specific Guidelines

Each language directory contains its own README with setup and tooling details.

Please ensure:
- Code follows the language’s formatting and linting rules
- Tests are added or updated where appropriate
- CI passes before submitting a PR

---

## 🧪 Testing

Before submitting a pull request, make sure:

### Python
```bash
cd Python
poetry install
poetry run ruff check .
poetry run pyright
poetry run pytest
```

(Go and Rust instructions will live in their respective READMEs.)

---

## 🔒 Security Issues

Please **do not open public issues** for security vulnerabilities.

Instead, follow the instructions in [`SECURITY.md`](SECURITY.md).

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

---

## 🙌 Code of Conduct

Be respectful, constructive, and professional.  
This project values thoughtful engineering and clear communication.

---

Thank you for helping make Specter better 🚀
