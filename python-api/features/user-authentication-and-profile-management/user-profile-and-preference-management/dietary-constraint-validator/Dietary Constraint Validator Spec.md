ROSETIC:153f1c40-befa-4df5-b059-72a5ddde5e1a

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
**Dietary Constraint Validator**

## Feature Description:
Validates incoming dietary and allergy data against a standardized medical and nutritional taxonomy to ensure data integrity and safety.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive raw dietary restriction input from API.

2. Normalize input against master taxonomy database.

3. Validate restriction against known allergen list.

4. Flag conflicting or ambiguous dietary entries.

5. Persist validated constraints to user profile store.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Allergy data must map to standardized medical codes.

- Conflicting dietary restrictions trigger validation errors.

