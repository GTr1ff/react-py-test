ROSETIC:2c8f25b0-7e64-4809-85e2-7b1b63cca176

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
**Inventory Categorization Engine**

## Feature Description:
Automatically classifies ingredients into logical groups to facilitate efficient pantry management and shopping list organization.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Analyze incoming ingredient metadata.

2. Map ingredient to predefined category taxonomy.

3. Assign storage condition attributes to item.

4. Update inventory record with category tags.

5. Index categorized items for search optimization.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Every ingredient must map to at least one primary category.

- Taxonomy updates require administrative approval.

