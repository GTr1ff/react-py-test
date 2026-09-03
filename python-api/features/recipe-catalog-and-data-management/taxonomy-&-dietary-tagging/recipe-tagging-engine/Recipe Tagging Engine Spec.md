ROSETIC:67eb08dd-5a13-4c00-b68f-314d9bc0df53

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
**Recipe Tagging Engine**

## Feature Description:
Automates the assignment of dietary and classification tags to recipes based on ingredient analysis and predefined business logic rules.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive recipe data from the lifecycle module.

2. Analyze ingredient list against dietary exclusion rules.

3. Map recipe attributes to taxonomy categories.

4. Apply calculated tags to the recipe record.

5. Log tagging audit trail for quality assurance.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Tags must map to existing entries in the registry.

- Conflicting dietary tags trigger manual review flags.

