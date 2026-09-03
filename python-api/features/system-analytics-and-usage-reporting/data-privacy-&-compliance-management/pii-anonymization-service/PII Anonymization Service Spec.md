ROSETIC:40615dd1-5f62-4c8a-af78-bb04b9551af8

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
**PII Anonymization Service**

## Feature Description:
Applies cryptographic hashing or masking techniques to sensitive user identifiers before data enters the analytical storage layer.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Intercept raw event stream from ingestion pipeline.

2. Identify fields containing personally identifiable information.

3. Apply deterministic hashing to sensitive identifiers.

4. Replace original values with anonymized tokens.

5. Forward sanitized data to the analytics warehouse.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Original PII must never be stored in the analytics warehouse.

- Hashing algorithms must use a secure, rotated salt.

