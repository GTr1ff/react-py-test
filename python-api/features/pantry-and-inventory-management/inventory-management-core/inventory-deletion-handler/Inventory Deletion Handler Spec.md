ROSETIC:45549cbe-9b79-4f89-b9de-b276426ffb7a

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
**Inventory Deletion Handler**

## Feature Description:
Manages the removal of inventory items while ensuring referential integrity across related system modules.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive request to delete inventory item.

2. Check for active dependencies in recommendation engine.

3. Archive record to historical storage.

4. Remove record from active inventory table.

5. Broadcast deletion event to dependent services.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Items linked to active meal plans require confirmation before deletion.

- Deleted records must be archived for historical reporting.

