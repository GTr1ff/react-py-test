ROSETIC:f31aa9ea-f313-4b2c-b201-ed1649eda7b5

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
**Session Revocation Manager**

## Feature Description:
Handles the immediate invalidation of active user sessions across all devices to ensure security during logout or account compromise events.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive session invalidation request for a specific user ID.

2. Identify all active session tokens associated with the user.

3. Blacklist identified tokens in the distributed cache.

4. Remove session metadata from the persistent storage layer.

5. Broadcast revocation event to all connected service instances.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Revocation must propagate to all system nodes within milliseconds.

- Blacklisted tokens must be rejected by all API gateways immediately.

