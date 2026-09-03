ROSETIC:9b7e2400-713a-477a-a10c-8292e163893e

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
**Identity Lifecycle Manager**

## Feature Description:
Manages the creation, suspension, and deletion of user accounts within the system registry.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive request to create new user identity.

2. Validate uniqueness of user identifier.

3. Provision account record in identity database.

4. Assign default security roles to new account.

5. Notify downstream systems of new identity creation.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- User identifiers must be globally unique.

- Accounts remain in suspended state until email verification.

