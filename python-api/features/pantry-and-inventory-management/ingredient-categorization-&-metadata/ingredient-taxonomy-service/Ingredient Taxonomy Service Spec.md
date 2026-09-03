ROSETIC:c5b7bc70-2bc4-4881-a5f6-5f8964f69e76

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
**Ingredient Taxonomy Service**

## Feature Description:
Manages the hierarchical classification structure for all inventory items to ensure consistent categorization across the system.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive request for new category creation.

2. Validate category hierarchy against existing schema.

3. Persist category record to the metadata database.

4. Update cached taxonomy tree for rapid retrieval.

5. Broadcast category change events to dependent services.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Categories must follow a strict parent-child hierarchy.

- Duplicate category names are prohibited within the same level.

