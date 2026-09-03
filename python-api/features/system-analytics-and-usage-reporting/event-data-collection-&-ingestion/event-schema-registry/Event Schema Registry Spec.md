ROSETIC:3be2494e-f709-4dc7-a9b4-533d17211741

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
**Event Schema Registry**

## Feature Description:
Maintains and enforces standardized event definitions to ensure consistency across all incoming telemetry data streams.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive schema registration request from developers.

2. Validate schema structure against predefined standards.

3. Store schema version in the central repository.

4. Publish schema updates to ingestion endpoints.

5. Reject non-compliant event payloads during ingestion.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All events must adhere to a registered schema version.

- Schema changes must maintain backward compatibility.

