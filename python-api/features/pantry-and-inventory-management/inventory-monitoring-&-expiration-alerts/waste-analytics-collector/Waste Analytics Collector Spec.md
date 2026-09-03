ROSETIC:0571c81f-f297-4b84-9df0-d01c7f6ba0da

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
**Waste Analytics Collector**

## Feature Description:
Tracks expired items that were not consumed to provide insights into household food waste patterns.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Detect items marked as expired in the inventory.

2. Capture item details and expiration timestamp.

3. Aggregate waste data into historical analytics storage.

4. Generate periodic waste summary reports for the user.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Waste data must be anonymized for system-wide trend analysis.

- Items manually removed before expiration are excluded from waste metrics.

