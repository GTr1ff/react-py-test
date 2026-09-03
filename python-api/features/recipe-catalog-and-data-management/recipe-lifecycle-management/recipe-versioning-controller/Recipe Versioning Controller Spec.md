ROSETIC:f7069148-7c03-4e06-b8cd-9bc2efc3e9a4

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
**Recipe Versioning Controller**

## Feature Description:
Manages historical snapshots and state transitions of recipe entities to ensure auditability and rollback capabilities.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Capture current recipe state upon update request.

2. Generate unique version identifier for the snapshot.

3. Store snapshot in the historical audit table.

4. Update the active recipe pointer to the new version.

5. Log the change event with timestamp and actor ID.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Every modification must increment the version number.

- Historical versions are immutable and read-only.

