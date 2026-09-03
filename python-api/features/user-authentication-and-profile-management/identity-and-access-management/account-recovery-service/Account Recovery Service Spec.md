ROSETIC:e81dda7e-6032-435b-885b-ca20bfc62b2b

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
**Account Recovery Service**

## Feature Description:
Orchestrates the secure reset of user credentials through verified communication channels.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive password reset request for user identity.

2. Generate unique time-limited recovery token.

3. Send recovery link to verified email or phone.

4. Validate recovery token upon link activation.

5. Update user password with new provided value.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Recovery tokens must be single-use only.

- Password history prevents reuse of last three passwords.

