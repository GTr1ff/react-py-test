ROSETIC:84c7ac82-cff5-4438-8021-2f933be5c802

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
**Multi-Factor Authentication Provider**

## Feature Description:
Generates and validates secondary verification codes to ensure identity assurance beyond primary credentials.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Trigger MFA challenge upon successful password verification.

2. Generate time-based one-time password or push notification.

3. Transmit verification code to registered user device.

4. Receive verification code from the client.

5. Validate code against current time window.

6. Issue temporary access token upon successful verification.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- MFA codes expire after five minutes.

- MFA is mandatory for all administrative accounts.

