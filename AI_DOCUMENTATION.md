# AI-Assisted Software Engineering — Task Execution & Artifacts

## 1. Task Breakdown & Engineering Output
- **Task 1: Architecture & Domain Partitioning:** Partitioned the microservice into FastAPI presentation handlers (`src/main.py`), pure domain logic (`src/service.py`), schema definitions (`src/models.py`), and thread-safe persistence (`src/repository.py`).
- **Task 2: API Contract Specification:** Authored `openapi.yaml` specifying endpoints, field validation rules, schemas, and error responses.
- **Task 3: Domain Implementation & Persistence:** Built Base62 key generation, atomic click increments, custom alias conflict detection, and database sequence initialization.
- **Task 4: Quality Gate & Test Coverage:** Designed test suites covering domain unit behavior, API integration contracts, click analytics, and thread concurrency.

---

## 2. Prompts & Iteration Logs

### A. Greenfield Example (Initial Boilerplate Generation)
- **Prompt:** *"Generate a modular FastAPI URL shortener service using Pydantic V2, custom domain exception hierarchy, and Base62 encoding."*
- **AI Output:** Basic FastAPI endpoints with in-memory dictionary storage.
- **Validation & Refactoring:** Rejected in-memory storage due to data loss across process restarts; refactored the persistence layer into a dedicated `SQLiteRepository`.

### B. Brownfield Example (Adding Concurrency & Database Persistence)
- **Prompt:** *"Refactor `repository.py` to use SQLite with WAL mode, busy timeouts, and atomic click counter updates."*
- **AI Output:** SQLite integration using single-threaded connections.
- **Validation & Refactoring:** Discovered lock contention when testing parallel requests; added `timeout=20.0`, `check_same_thread=False`, and SQLite WAL mode.

### C. Ambiguous Requirement Resolution
- **Requirement Gap:** The specification did not explicitly define how custom alias conflicts should behave when two concurrent requests submit the same alias simultaneously.
- **Engineering Decision:** Implemented a service-level `threading.Lock()` alongside a database `PRIMARY KEY` constraint to guarantee single-winner creation and return a clean HTTP `400 Bad Request` on duplicate entries.

---

## 3. Ownership & Trade-off Summary
- **Single-Instance SQLite vs. Distributed Storage:** Selected SQLite with WAL mode to provide a zero-dependency local execution environment that satisfies persistence requirements. For multi-instance horizontal scaling, `SQLiteRepository` can be swapped for a distributed store like PostgreSQL or Redis.
