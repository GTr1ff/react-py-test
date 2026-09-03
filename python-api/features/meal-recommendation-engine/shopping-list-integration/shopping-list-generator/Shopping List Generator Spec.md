ROSETIC:e66911ab-7b88-4b26-8af2-01cfc0625e1f

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
**Shopping List Generator**

## Feature Description:
Calculates the delta between selected recipe requirements and current pantry inventory to identify necessary items for purchase.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive selected recipe ingredient requirements.

2. Query current inventory levels for required ingredients.

3. Calculate quantity gaps for missing or insufficient items.

4. Format missing items into a structured list.

5. Persist the generated list to the user shopping store.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Exclude ingredients marked as pantry staples.

- Aggregate quantities for identical ingredients across multiple recipes.

