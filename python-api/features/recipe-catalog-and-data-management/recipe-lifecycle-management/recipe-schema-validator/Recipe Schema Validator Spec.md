ROSETIC:841ad6e0-30c0-4f88-80fe-66b5a7e913ed

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
**Recipe Schema Validator**

## Feature Description:
Enforces structural integrity and data consistency for all incoming recipe payloads before persistence into the central repository.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive raw recipe data payload.

2. Parse payload against predefined JSON schema.

3. Validate mandatory fields and data types.

4. Check ingredient references against master database.

5. Return validation status to the caller.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All recipes must contain at least one preparation step.

- Ingredient units must match the master unit registry.

