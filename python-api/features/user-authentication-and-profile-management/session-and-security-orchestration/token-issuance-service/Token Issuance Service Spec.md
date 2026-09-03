ROSETIC:2969571c-cf33-4906-a2e6-52eb6aa79c8a

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
**Token Issuance Service**

## Feature Description:
Generates and signs secure authentication tokens upon successful identity verification to facilitate stateless session management across distributed system components.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive authentication success signal from identity provider.

2. Generate cryptographically secure access and refresh tokens.

3. Embed user identity and scope claims into token payload.

4. Sign tokens using secure server-side private keys.

5. Return tokens to the requesting client application.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Tokens must expire within a defined short-lived duration.

- Refresh tokens must be stored in a secure database with revocation capability.

