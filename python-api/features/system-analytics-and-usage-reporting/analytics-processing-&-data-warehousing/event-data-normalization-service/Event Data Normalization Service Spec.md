ROSETIC:57d4ed50-1ad3-4c3d-b799-d02c137eef57

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
**Event Data Normalization Service**

## Feature Description:
Standardizes raw event payloads into a unified schema to ensure consistency across disparate data sources before storage.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Read raw event messages from the ingestion queue.

2. Validate event structure against the master schema.

3. Map heterogeneous fields to normalized data types.

4. Enrich event records with metadata and timestamps.

5. Route normalized events to the staging storage.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Discard events failing schema validation.

- Maintain strict field mapping consistency.

