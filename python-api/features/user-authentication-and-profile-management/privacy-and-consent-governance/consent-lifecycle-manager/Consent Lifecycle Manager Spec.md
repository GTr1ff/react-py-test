ROSETIC:6c7388ff-20ea-4641-9c5c-d67acedb4c6d

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
**Consent Lifecycle Manager**

## Feature Description:
Tracks and updates user consent status for specific data processing activities across the platform.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive consent request from client application.

2. Validate request against current privacy policy version.

3. Update consent status in the central database.

4. Publish consent change event to message bus.

5. Return confirmation status to the requester.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Consent must be explicitly recorded for each data category.

- Consent records must include a timestamp and policy version ID.

