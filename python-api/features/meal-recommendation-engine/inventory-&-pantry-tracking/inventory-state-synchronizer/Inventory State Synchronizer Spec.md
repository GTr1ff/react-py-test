ROSETIC:8286a35d-dc9a-4514-9c5b-b2445f3af752

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
**Inventory State Synchronizer**

## Feature Description:
Maintains the current state of ingredient quantities and metadata by processing incoming updates from various input sources.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive inventory update request from client.

2. Validate ingredient existence in master database.

3. Calculate new quantity based on delta.

4. Persist updated state to inventory store.

5. Publish inventory change event to message bus.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Negative quantities are prohibited for tracked items.

- Updates must be atomic to prevent race conditions.

