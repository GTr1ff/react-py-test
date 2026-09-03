ROSETIC:b9ec3688-3318-4fba-b25e-ac6308e7e7ca

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
**Threat Detection Engine**

## Feature Description:
Analyzes login patterns and session activity in real-time to identify and mitigate potential unauthorized access or brute-force attempts.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Ingest authentication attempt logs from the gateway.

2. Calculate risk score based on IP reputation and velocity.

3. Compare current activity against established user behavior baselines.

4. Trigger security alerts upon detection of anomalous patterns.

5. Enforce temporary account lockout for high-risk activity.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Failed login attempts must trigger exponential backoff delays.

- Anomalous logins from new geographic locations require secondary verification.

