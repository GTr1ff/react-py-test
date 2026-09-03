ROSETIC:2b36eba3-9f21-4db4-812a-daa1c20afd8d

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
Enforces strict filtering rules against recipe ingredients based on user-defined health restrictions and allergy profiles.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive user dietary profile data.

2. Map profile constraints to ingredient exclusion lists.

3. Filter recipe candidates against exclusion lists.

4. Flag incompatible recipes for exclusion.

5. Return validated recipe list to engine.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Allergy constraints must always override preference settings.

- Invalid dietary inputs trigger an immediate system error.

