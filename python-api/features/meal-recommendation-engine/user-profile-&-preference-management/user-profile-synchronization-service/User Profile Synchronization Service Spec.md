ROSETIC:78231637-417d-4731-a9b0-aa20874891b3

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
**User Profile Synchronization Service**

## Feature Description:
Maintains consistency of user preference data across distributed storage nodes and caching layers.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Detect updates to user profile records.

2. Validate schema integrity of updated data.

3. Persist changes to the primary database.

4. Invalidate stale user preference cache entries.

5. Broadcast update events to downstream services.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Profile updates must be atomic to prevent partial data states.

- Cache invalidation must occur within milliseconds of database commit.

