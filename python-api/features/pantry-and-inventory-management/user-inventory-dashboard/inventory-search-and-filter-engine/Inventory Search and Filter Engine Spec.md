ROSETIC:62596b3d-09d6-4de3-911a-3d4e9ed145ca

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
**Inventory Search and Filter Engine**

## Feature Description:
Processes complex search queries and filter criteria to return subsets of inventory items based on user-defined parameters.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive search terms and filter criteria from the client.

2. Parse query parameters into database search predicates.

3. Execute filtered queries against the inventory data store.

4. Apply pagination logic to the resulting dataset.

5. Return the filtered list to the dashboard interface.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Search must support partial string matching on ingredient names.

- Filters must be applied cumulatively.

