[![CI](https://github.com/XOR0831/Specter/actions/workflows/python-ci.yml/badge.svg)](https://github.com/XOR0831/Specter/actions/workflows/python-ci.yml) ![Python](https://img.shields.io/badge/python-3.11-blue) ![License](https://img.shields.io/github/license/XOR0831/Specter)
![Coverage](https://codecov.io/gh/XOR0831/Specter/branch/main/graph/badge.svg)




# Specter

**Specter** is a modern, production-grade **port scanner and service fingerprinter** built in Python.

It is designed to be:
- Fast
- Safe by default
- Modular
- Extensible
- Suitable for real-world infrastructure and homelabs

Specter focuses on **clarity, correctness, and architecture**, not exploit payloads.

> ⚠️ **Use this tool only on systems you own or are explicitly authorized to test.**

---

## ✨ Features

- ✅ TCP port scanning (connect scan)
- ✅ Optional UDP scanning
- ✅ Host discovery (ICMP + TCP fallback)
- ✅ Service banner grabbing
- ✅ Service & version fingerprinting
- ✅ TLS certificate inspection (HTTPS)
- ✅ Rate limiting (safe defaults)
- ✅ Rich, human-readable CLI output
- ✅ JSON output for automation
- ✅ Modular, testable architecture

---

## 🧠 Philosophy

Specter is built with the same principles used in **professional security tooling**:

- Clear separation of concerns
- Predictable behavior
- Ethical scanning defaults
- Clean CLI UX
- Strong typing and structure
- Easy to extend without rewrites

This is **not** a one-file script.  
It is a **system**.

---

## 📦 Installation

### Requirements
- Python **3.11+**
- `poetry`
- (Optional) Root privileges for ICMP ping

---

### Install Poetry (recommended)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or with pipx:

```bash
pipx install poetry
```

---

### Install Dependencies

```bash
poetry install
```

---

## ▶️ Usage

You can run Specter either via **Poetry** or as a local CLI after installation.

---

### Show Help

```bash
specter --help
```

Or via Poetry:

```bash
poetry run specter --help
```

---

## 🔍 Scan Hosts & Ports

### Basic Scan

Scan a single host with default ports (`1–1024`):

```bash
specter scan 192.168.1.1
```

---

### Scan Specific Ports

```bash
specter scan 192.168.1.1 -p 22,80,443
```

Supported port formats:
- `22`
- `22,80,443`
- `1-1024`
- `22,80-90,443`

---

### Scan a CIDR Range

```bash
specter scan 192.168.1.0/24
```

---

### Scan Targets from a File

```bash
specter scan targets.txt
```

Example `targets.txt`:

```text
# comments are ignored
192.168.1.1
192.168.1.0/24
example.com
```

---

## 🌐 Host Discovery

Discover live hosts **without scanning ports**:

```bash
specter discover 192.168.1.0/24
```

Skip discovery during scans:

```bash
specter scan 192.168.1.1 --no-ping
```

---

## 📡 UDP Scanning

Enable UDP scanning (results may be `open|filtered`):

```bash
specter scan 192.168.1.1 --udp
```

---

## 🧪 Service Detection

Service fingerprinting is **enabled by default**.

Disable it if you only want port states:

```bash
specter scan 192.168.1.1 --no-service-detect
```

---

## 📤 Output Formats

### Human-Readable Table (Default)

```bash
specter scan 192.168.1.1
```

Example output:

```text
Host: 192.168.1.1

Port   Proto  State     Service  Version
22     tcp    open      ssh      8.9p1
80     tcp    open      nginx    1.24.0
```

---

### JSON Output

```bash
specter scan 192.168.1.1 --json
```

Write JSON to a file:

```bash
specter scan 192.168.1.1 --json -o results.json
```

---

## ⚙️ Performance & Safety Options

### Rate Limiting

```bash
specter scan 192.168.1.1 --rate-limit 1000
```

---

### Timeout & Retries

```bash
specter scan 192.168.1.1 --timeout 3 --retries 2
```

---

## 🪵 Logging & Debugging

### Verbose Mode

```bash
specter scan 192.168.1.1 --verbose
```

---

### Debug Mode (Development)

```bash
specter --debug scan 192.168.1.1
```

---

## 🔐 Permissions Note

Some features (ICMP ping) require elevated privileges.

Run with:

```bash
sudo specter scan 192.168.1.1
```

Or skip discovery:

```bash
specter scan 192.168.1.1 --no-ping
```

---

## 🏗️ Project Structure

```text
scanner/
├── cli/          # CLI commands (Typer)
├── core/         # Scan orchestration
├── protocols/    # TCP / UDP / ICMP logic
├── fingerprint/  # Banner grabbing & signatures
├── output/       # Table & JSON output
├── utils/        # Shared helpers
└── tests/        # Test suite
```

Each layer has a **single responsibility** and does not leak concerns.

---

## 🧪 Testing

Run tests with:

```bash
poetry run pytest
```

Tests focus on:
- Input parsing
- Signature matching
- Target expansion
- Rate limiting behavior

---

## 🚀 Roadmap

Planned / optional future enhancements:

- Async scanning engine
- TCP SYN scans (raw sockets)
- Plugin system for fingerprints
- Config file support (`~/.specter/config.yaml`)
- Distributed scanning agents
- Web UI / dashboard
- Prometheus metrics export

---

## 📜 License

MIT License  
© 2025 Daniel Soriano

---

## ⚠️ Disclaimer

This software is provided for **educational and authorized security testing purposes only**.

The author is not responsible for misuse or damage caused by this tool.
