ROSETIC:e514dcdc-4d63-4334-a378-8b44b85867de

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
**Dashboard Cache Manager**

## Feature Description:
Caches frequently accessed analytical results to reduce load on the data warehouse and improve dashboard responsiveness.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Intercept incoming dashboard query requests

2. Check cache for existing valid result set

3. Return cached data if TTL is valid

4. Fetch fresh data if cache miss occurs

5. Update cache store with new result set


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Cache TTL must not exceed 24 hours

- Cache invalidation must occur upon data updates

