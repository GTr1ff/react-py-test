ROSETIC:04122160-c29a-44de-9bb9-a987943fcb27

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
**Consent Lifecycle Manager**

## Feature Description:
Tracks and manages user-granted permissions for data collection and processing activities to ensure regulatory compliance.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive consent state change from client application.

2. Validate consent payload against current schema.

3. Persist consent record in immutable audit store.

4. Broadcast consent update to downstream data processors.

5. Return confirmation status to the requesting service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Consent must be explicitly recorded for each data category.

- Withdrawal of consent must propagate to all downstream systems within 24 hours.

