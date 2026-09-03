ROSETIC:b14fef4f-826d-4f67-a44e-7b304c1c3558

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
**Shopping List Categorizer**

## Feature Description:
Organizes shopping list items into logical store sections to optimize the physical shopping experience.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch raw list of missing ingredients.

2. Map each ingredient to a predefined store category.

3. Group items by their assigned category.

4. Sort categories based on standard store layouts.

5. Return the categorized list for display.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Assign default category if mapping is unavailable.

- Maintain alphabetical order within each category.

