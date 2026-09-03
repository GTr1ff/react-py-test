ROSETIC:b7389956-b5f9-4867-a678-9b50c4352b54

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
**Inventory Quantity Synchronizer**

## Feature Description:
Handles atomic updates to ingredient quantities to prevent race conditions during concurrent inventory modifications.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Lock the specific inventory record row.

2. Calculate the new quantity based on input.

3. Verify the resulting quantity is non-negative.

4. Update the record with the new value.

5. Release the row lock.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Quantity values cannot be negative.

- Concurrent updates must be serialized per item.

