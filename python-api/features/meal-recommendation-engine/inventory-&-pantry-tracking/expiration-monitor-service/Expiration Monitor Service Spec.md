ROSETIC:c7fd721c-596b-4ea4-8177-3a3c38f89c9c

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
**Expiration Monitor Service**

## Feature Description:
Tracks ingredient shelf-life and triggers notifications when items approach their expiration dates to minimize food waste.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Scan inventory records for near-expiry items.

2. Filter items based on user-defined thresholds.

3. Generate expiration alert for identified items.

4. Dispatch alert to notification service.

5. Mark items as expired in inventory database.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Alerts must trigger at least 48 hours before expiration.

- Expired items must be flagged for removal from recommendations.

