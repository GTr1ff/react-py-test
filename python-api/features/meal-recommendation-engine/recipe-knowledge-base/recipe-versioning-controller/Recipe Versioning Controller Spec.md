ROSETIC:96d9472f-da7b-4f05-96e2-09da3d040cd9

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
Manages historical versions of recipe data to ensure auditability and stability for active recommendation sessions.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Capture snapshots of recipe data upon modification.

2. Assign unique version identifiers to each record.

3. Archive previous versions in cold storage.

4. Maintain pointers to the current active version.

5. Restore historical versions upon system rollback requests.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Active recommendations must reference a fixed version.

- Historical data must be retained for seven years.

