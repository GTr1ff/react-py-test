ROSETIC:6e206604-aedb-4609-9aa1-9e4383d8aa19

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
**Quick Action Orchestrator**

## Feature Description:
Coordinates state transitions for common inventory tasks triggered by dashboard buttons such as marking items as used or adding to lists.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Capture the action request and target item identifier.

2. Validate the requested state transition against business rules.

3. Invoke the appropriate backend service to update the record.

4. Confirm the successful execution of the state change.

5. Broadcast a refresh event to update the dashboard UI.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Actions must be idempotent to prevent duplicate processing.

- Unauthorized state transitions are rejected immediately.

