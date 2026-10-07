# AI-Assisted Software Engineering — URL Shortener Service

[![CI Quality Gate](https://github.com/abhishek-sb-devops/ai-proficient-se/actions/workflows/ci.yml/badge.svg)](https://github.com/abhishek-sb-devops/ai-proficient-se/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![Code Style](https://img.shields.io/badge/code%20style-flake8-green)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)

A production-ready, high-performance URL shortener microservice built with **Python 3.13**, **FastAPI**, **SQLite**, and **Docker**. This project demonstrates how AI-assisted workflows can accelerate software delivery while maintaining strict domain boundaries, thread safety, and test coverage.

---

## 📁 Project Directory Structure

```text
ai-proficient-se/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline (Linting & Pytest)
├── src/                       # Application Source Code
│   ├── __init__.py
│   ├── config.py              # Environment & Pydantic settings
│   ├── encoder.py             # Base62 encoding utility
│   ├── exceptions.py          # Custom domain exception hierarchy
│   ├── main.py                # FastAPI entrypoint & health routes
│   ├── middleware.py          # Request correlation ID middleware
│   ├── models.py              # Pydantic schemas aligned with OpenAPI spec
│   ├── repository.py          # Thread-safe SQLite persistence layer
│   └── service.py             # Core domain service & thread-locked alias management
├── tests/                     # Automated Test Suite
│   ├── __init__.py
│   ├── test_api.py            # Integration tests (HTTP endpoints, contract, concurrency)
│   └── test_service.py        # Unit tests (encoder, repository, domain logic)
├── AI_DOCUMENTATION.md        # AI workflow, prompts, and engineering trade-offs
├── Dockerfile                 # Production container build
├── openapi.yaml               # OpenAPI 3.0 API Specification
├── pyproject.toml             # Flake8 & Pytest configuration
├── requirements.txt           # Production Python dependencies
└── README.md                  # Project documentation

🚀 Key Features & Architecture
Persistent Storage: SQLite database backend with Write-Ahead Logging (WAL) and busy timeouts, ensuring data durability across container restarts.

Concurrency & Thread Safety: Thread-safe custom alias assignment guaranteed via threading.Lock() at the service layer and PRIMARY KEY constraints at the database layer.

OpenAPI 3.0 Alignment: Fully aligned request payload schemas (original_url), response payloads (short_code, original_url, created_at), and status codes (400 Bad Request for conflicts).

Observability: Structured JSON logging, /healthz and /readyz probes, and X-Correlation-ID header request tracing.

AI Execution Artifacts: Detailed documentation in AI_DOCUMENTATION.md outlining greenfield/brownfield prompts, iteration logs, and engineering trade-offs.

🛠️ Getting Started
Prerequisites
Python 3.11+
Docker (optional)

Local Setup & Installation

Clone the repository:

git clone [https://github.com/abhishek-sb-devops/ai-proficient-se.git](https://github.com/abhishek-sb-devops/ai-proficient-se.git)
cd ai-proficient-se

Create and activate a virtual environment:

python -m venv venv
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

Install dependencies:
install -r requirements.txt

Run the local development server:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
The service will be available at http://localhost:8000. Access interactive API documentation at http://localhost:8000/docs.

🧪 Testing & Linting

Run the Test SuiteThe repository includes unit tests (tests/test_service.py) and HTTP 

integration/concurrency tests (tests/test_api.py):
python -m pytest -v tests/

Run Code LinterEnforce code formatting and line-length standards:
python -m flake8 src/ tests/ --max-line-length=100

🐳 Docker Deployment
Build the ImageBashdocker build -t url-shortener .

Run the Container:
docker run -d -p 8000:8000 --name url-shortener-app url-shortener

Verify Service HealthBashcurl http://localhost:8000/healthz

📋 API Endpoints SummaryMethodEndpointDescriptionStatus CodeGET/healthzLiveness health probe200 OKGET/readyzReadiness health probe200 OKPOST/api/v1/shortenShorten a URL or set a custom alias201 Created / 400 Bad RequestGET/{short_code}Redirect to original target URL302 Found / 404 Not FoundGET/api/v1/analytics/{short_code}Retrieve analytics (click count)200 OK / 404 Not Found
