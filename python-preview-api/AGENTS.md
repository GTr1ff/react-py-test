# Feature Implementation Instructions

## Purpose of the Agent

Before implementing any feature:

1. Read README.md at the project root for project-specific setup, conventions, and onboarding notes.
2. Read the relevant spec.md for the feature you are implementing.
3. Read the codebase (if available) to understand what is already in place — reuse existing functionality wherever applicable.

Then implement the described feature end-to-end **in a single code-generation pass**:

- Follow the provided steps in the exact order and ensure rules are strictly respected.
- Adhere to the Core Principles.
- Follow the Python enviorment setup.
- Produce clean, secure, and maintainable code using best engineering practices.
- Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
- Clearly state assumptions when needed.
- Do not invent or change the given steps or rules — they are authoritative.
- If something is ambiguous, make reasonable, production-quality design decisions and explain them briefly.
- If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.
- Stop after code generation is complete.
---

## Python Environment Setup

- Before writing any code, ensure the project has a working Python virtual environment:

Check if a virtual environment already exists (typically .venv/ or venv/ at the project root).
If one does not exist, create one: python -m venv .venv
Confirm that dependencies are installed from requirements.txt (or equivalent): pip install -r requirements.txt
Confirm that pytest is available in the environment. If it is not listed in the project dependencies, install it: pip install pytest

Do this once at the start. Do not re-run environment setup between files or after code generation is complete.

# Guidance for the LLM

## Core Principles

### I. Feature-Oriented Architecture (FOA)
Every feature MUST be organized in the `features/{feature_name}` structure with complete separation of concerns: models, repository, service, router, schemas, and tests. Each feature MUST be independently testable and deployable. No cross-feature imports except through well-defined service interfaces. The `FeatureLocator` pattern ensures automatic discovery and registration of all features. Shared infrastructure (e.g. pagination utilities, logging, exceptions, JSON converters) MUST live under `/core` and MUST NOT be duplicated in feature folders.

**Rationale**: Maintains modularity, enables parallel development, and ensures consistent project structure across all team members.

#### Structure 

features/
  {feature_name}/
    models.py        # SQLAlchemy ORM models
    repository.py    # Data access layer
    service.py       # Business logic
    router.py        # Handles HTTP concerns 
    schemas.py       # Pydantic request / response schemas
    tests/
      test_models.py
      test_repository.py
      test_service.py
      test_router.py


### II. Layered Clean Architecture
The architecture MUST maintain strict separation: Router → Service → Repository → Model. Repositories handle only data access with SQLAlchemy. Services contain business logic and coordinate between repositories. Routers handle HTTP concerns only. Models define database schema with proper relationships. Schemas define API contracts with Pydantic validation.

**Rationale**: Clear separation of concerns enables maintainability, testability, and allows independent evolution of each layer.


### III. API Contract Discipline
All API endpoints MUST define request/response schemas using Pydantic models. HTTP status codes MUST follow REST conventions (200 for success, 201 for creation, 404 for not found, 422 for validation errors). Pagination MUST use the standardized `PaginationRequest`/`PaginatedResponse` pattern. All endpoints MUST include proper error responses and documentation.

**Rationale**: Consistent API contracts improve developer experience, enable automatic documentation generation, and ensure predictable client integration.


### IV. Code Quality Requirements
- Import statements MUST be organized: standard library, third-party, local imports

Example:
```
import os
import requests
from my_project.database import get_user_by_id
```

- Type hints MUST be used for all function parameters and return values

Example:
`def fetch_user_profile(user_id: int) -> dict:`

- Docstrings MUST follow Google format for all public methods

Example:
```
"""
Fetches a user's profile from an external API.

Args:
    user_id (int): The ID of the user to fetch.

Returns:
    dict: A dictionary containing the user's profile data.
"""
```

- Variable names MUST be descriptive and follow snake_case convention

Example:
```
api_url = f"https://api.example.com/users/{user.username}"
```



### V. Testing Requirements
- Test coverage MUST be maintained at minimum 90% for all feature modules
- Test files MUST be contained in their respective feature folder and mirror the source structure: `{feature_name}/tests/test_{module}.py`
- Each test MUST follow Arrange-Act-Assert pattern with clear sections
- Mock objects MUST be used for external dependencies in unit tests
- Parametrized tests MUST be used for testing multiple scenarios
- Do not run/validate test until you are done implementing them
- Tests MUST be pure Python tests and rely only on standard import semantics
- Tests MUST NOT compute file paths to application modules. Usage of `Path(__file__)`, `.parents[...]`, or hard-coded directory traversal to locate source files is forbidden.
- After implementing them run the test to make sure they are working.

---