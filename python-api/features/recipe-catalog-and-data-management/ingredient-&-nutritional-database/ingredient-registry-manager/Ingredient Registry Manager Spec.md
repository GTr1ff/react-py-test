ROSETIC:6b53b1d1-2fa5-41f7-a13f-79098b4293ea

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
**Ingredient Registry Manager**

## Feature Description:
Maintains the authoritative master list of raw ingredients and their baseline nutritional properties.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Accept requests for new ingredient definitions.

2. Verify ingredient uniqueness within the registry.

3. Assign standardized metadata and nutritional baselines.

4. Update the master index for search availability.

5. Notify dependent services of registry modifications.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Duplicate ingredient entries are strictly prohibited.

- Nutritional data must be sourced from verified databases.

