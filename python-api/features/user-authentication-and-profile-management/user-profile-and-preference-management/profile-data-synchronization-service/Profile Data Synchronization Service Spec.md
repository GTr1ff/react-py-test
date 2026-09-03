ROSETIC:cf899075-df5d-4e93-bc8a-f698cd3823d0

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
**Profile Data Synchronization Service**

## Feature Description:
Synchronizes user profile updates across distributed read-replicas and downstream analytical systems to maintain data consistency.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Detect write operation on user profile record.

2. Propagate changes to regional read-replicas.

3. Transform profile data for analytical schema.

4. Push updates to downstream data warehouse.

5. Confirm synchronization status to source service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Synchronization must complete within sub-second latency.

- Failed sync attempts must trigger retry logic.

