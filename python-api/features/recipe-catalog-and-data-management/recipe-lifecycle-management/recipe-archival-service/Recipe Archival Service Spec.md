ROSETIC:6cc1755a-17a7-4839-b8d2-cda441d3b993

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
**Recipe Archival Service**

## Feature Description:
Handles the logical deletion and lifecycle transition of deprecated or obsolete recipe content within the system.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive request to archive specific recipe ID.

2. Verify recipe status is not currently in use.

3. Update recipe status to archived in database.

4. Remove recipe from active search index.

5. Notify downstream services of archival event.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Archived recipes remain in the database for audit purposes.

- Archived recipes cannot be modified without restoration.

