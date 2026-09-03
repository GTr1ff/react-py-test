ROSETIC:dd2d2a6f-2a7d-4822-8d84-28311f48fae0

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
**Nutritional Calculation Engine**

## Feature Description:
Computes aggregate nutritional values for recipes based on ingredient composition and standardized serving sizes.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Retrieve ingredient list for a specific recipe.

2. Fetch nutritional profiles for each ingredient.

3. Apply scaling factors based on ingredient quantities.

4. Sum nutritional values across all recipe components.

5. Store calculated totals in the recipe metadata store.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Calculations must account for ingredient preparation loss factors.

- Total nutrition must be recalculated upon any ingredient update.

