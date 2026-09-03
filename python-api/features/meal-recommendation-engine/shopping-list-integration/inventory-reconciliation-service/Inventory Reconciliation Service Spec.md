ROSETIC:d85a0648-5264-462d-b79a-e15aaba0fd67

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
**Inventory Reconciliation Service**

## Feature Description:
Updates the user's pantry inventory records once items from the shopping list are confirmed as purchased.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive confirmation of purchased items.

2. Identify corresponding inventory records for each item.

3. Increment inventory quantities based on purchase data.

4. Update expiration dates for newly added items.

5. Broadcast inventory update events to the recommendation engine.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Validate purchase quantities against expected units.

- Trigger inventory alerts for items reaching minimum thresholds.

