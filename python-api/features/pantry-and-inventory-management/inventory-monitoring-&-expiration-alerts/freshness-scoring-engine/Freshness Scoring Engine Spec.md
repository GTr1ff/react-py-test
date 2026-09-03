ROSETIC:e7572b1d-eb0a-45b2-af16-6a3e2043ac1e

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
**Freshness Scoring Engine**

## Feature Description:
Calculates a freshness weight for inventory items to influence recipe prioritization in the recommendation engine.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Calculate remaining shelf life for each inventory item.

2. Normalize shelf life into a standardized freshness score.

3. Update item metadata with the calculated freshness value.

4. Broadcast freshness updates to the recommendation engine.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Expired items receive a zero freshness score.

- Freshness scores are recalculated daily or upon inventory update.

