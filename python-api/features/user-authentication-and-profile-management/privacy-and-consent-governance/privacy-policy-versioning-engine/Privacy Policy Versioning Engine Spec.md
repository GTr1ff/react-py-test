ROSETIC:c6185641-6b95-4e97-89e3-9debd63c02e3

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
**Privacy Policy Versioning Engine**

## Feature Description:
Maintains historical versions of privacy policies and maps them to active user consent records.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Store new policy text and effective date.

2. Assign unique version identifier to policy.

3. Flag existing consent records as requiring re-acceptance.

4. Serve current policy version to client applications.

5. Archive deprecated policy versions for audit.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Users must be prompted to re-consent upon major policy updates.

- Historical policy versions must remain immutable.

