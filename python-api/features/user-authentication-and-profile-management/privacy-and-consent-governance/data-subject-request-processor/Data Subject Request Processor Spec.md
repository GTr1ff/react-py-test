ROSETIC:030c35e6-3c4c-45f2-b491-0c7a25c639be

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
**Data Subject Request Processor**

## Feature Description:
Automates the fulfillment of data access, portability, and deletion requests from registered users.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Queue incoming data subject request.

2. Verify user identity against authentication service.

3. Aggregate user data from all registered microservices.

4. Format data into a secure exportable package.

5. Notify user of request completion status.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Data deletion requests must trigger cascading removal across all services.

- Exported data must be encrypted at rest.

