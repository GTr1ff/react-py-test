ROSETIC:4af885cb-33b4-40eb-956c-c427d47ea039

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
**Concurrent Session Controller**

## Feature Description:
Enforces policies regarding the maximum number of simultaneous active sessions allowed per user account to prevent credential sharing.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Intercept new session creation requests.

2. Query current active session count for the user.

3. Compare count against the configured maximum threshold.

4. Terminate the oldest session if the limit is exceeded.

5. Authorize the creation of the new session.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Maximum concurrent sessions per user is limited to five.

- System administrators can override session limits for specific account types.

