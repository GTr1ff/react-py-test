ROSETIC:7015f6f8-6282-4629-b8cb-ea1186d48f77

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
**Taxonomy Schema Registry**

## Feature Description:
Maintains the hierarchical structure and definitions of all classification categories, dietary labels, and metadata tags used across the recipe catalog.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Define new category hierarchy in the registry.

2. Validate schema constraints for tag relationships.

3. Persist taxonomy structure to the metadata store.

4. Broadcast schema update events to dependent services.

5. Version the taxonomy schema for backward compatibility.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Category identifiers must be globally unique.

- Circular dependencies in hierarchy are prohibited.

