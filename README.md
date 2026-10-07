# AI-Assisted Software Engineering — URL Shortener Prototype

This repository demonstrates how AI tools can accelerate software development while maintaining strict engineering control, robust architecture, and code quality.

## 📁 Project Directory Structure

```text
ai-proficient-se-assignment/
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline (Linting & Pytest)
│
├── app/                            # Domain-Driven Application Tier
│   ├── __init__.py
│   ├── config.py                   # Environment & Pydantic settings
│   ├── exceptions.py               # Custom domain exception hierarchy
│   ├── models.py                   # Pydantic schemas & DTOs
│   ├── encoder.py                  # Base62 encoding utility
│   ├── repository.py               # Repository abstraction & Thread-safe store
│   ├── service.py                  # Core domain service layer
│   ├── middleware.py               # Request correlation ID middleware
│   └── main.py                     # FastAPI application entrypoint & health endpoints
│
├── tests/                          # Automated Pytest Suite
│   ├── __init__.py
│   ├── test_encoder.py             # Base62 encoder unit tests
│   └── test_service.py             # Domain service & concurrency integration tests
│
├── docs/                           # API Contracts & Artifacts
│   ├── openapi.yaml                # OpenAPI 3.0 specification contract
│   └── postman_collection.json     # Ready-to-import Postman test suite
│
├── Dockerfile                      # Production container image build
├── docker-compose.yml              # Single-command local container orchestration
├── README.md                       # Architectural overview & guide
├── requirements.txt                # Production Python dependencies
├── pyproject.toml                  # Flake8 & Pytest configuration
└── .gitignore                      # Git exclusion rules

# AI-Assisted Software Engineering — URL Shortener Service

![CI Quality Gate](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)
![Code Style](https://img.shields.io/badge/code%20style-flake8-green)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)

## Architecture & Design
- **Base62 Encoding:** Uses Base62 character encoding on an auto-incrementing ID for deterministic short keys.
- **Thread Safety:** Thread-safe counter increments and analytics tracking via mutex locks.
- **Validation:** Enforces URI schemes (`http`/`https`) and sanitizes custom alias strings via regex (`^[a-zA-Z0-9_-]{3,30}$`).
- **OpenAPI 3.0 Contract:** Complete API specification located in `docs/openapi.yaml`.

## Project Structure
- `src/encoder.py`: Base62 encoding utility.
- `src/service.py`: URL Shortener domain service.
- `main.py`: Runnable entrypoint demonstrating real use cases.
- `tests/test_service.py`: Comprehensive Pytest test suite.
- `.github/workflows/ci.yml`: Automated CI quality gate.

## Getting Started

### Prerequisites
- Python 3.9+

### Installation & Run
```bash
pip install -r requirements.txt
python main.py