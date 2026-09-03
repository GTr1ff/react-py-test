ROSETIC:137ef0b9-4e31-408a-986c-4456be10a032

# Feature Implementation Instructions

You are an expert software engineer responsible for implementing the following application feature.
Follow the provided *steps* in the exact order and ensure *rules* are strictly respected.
Adhere to the provided *Core Principles*.
Produce clean, secure, and maintainable code using best engineering practices.
Clearly state assumptions when needed.
Do not invent or change the given steps or rules — they are authoritative.
If something is ambiguous, make reasonable, production-quality design decisions and explain them briefly.

---

## Feature Name:
**Query Orchestration Service**

## Feature Description:
Translates high-level dashboard requests into optimized analytical queries for the underlying data warehouse.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive visualization request from dashboard client

2. Parse request parameters into internal query format

3. Validate user access permissions for requested data

4. Route query to appropriate data warehouse partition

5. Format raw result set for frontend consumption


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Queries must execute within defined latency thresholds

- Unauthorized data access requests must be rejected

