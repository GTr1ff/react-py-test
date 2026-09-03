ROSETIC:27a00aaf-d42f-467f-ab1a-8fea1cda3a2d

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
**Event Integrity Validator**

## Feature Description:
Performs real-time sanitization and structural validation on ingested events to ensure data quality before storage.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Consume raw event batches from the buffer.

2. Parse event payloads against registered schemas.

3. Filter out malformed or corrupted data packets.

4. Route invalid events to a dead-letter queue.

5. Forward validated events to the processing pipeline.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Malformed events must be quarantined for inspection.

- Validation must occur within milliseconds of ingestion.

