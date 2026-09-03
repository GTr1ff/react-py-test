ROSETIC:0a0469a5-b08d-40fb-b646-b36c44e798b0

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
**Expiration Date Validator**

## Feature Description:
Enforces business logic for date integrity when users add or modify expiration dates for perishable inventory items.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive expiration date update request.

2. Compare input date against current system date.

3. Flag dates set in the past as invalid.

4. Format date according to system standards.

5. Persist validated date to the inventory record.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Expiration dates cannot be set in the past.

- Null expiration dates are permitted for non-perishable items.

