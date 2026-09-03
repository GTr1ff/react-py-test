ROSETIC:31587a4a-f947-4d24-95e8-9315050b9d3c

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
**API Response Caching Layer**

## Feature Description:
Stores frequently accessed recipe data to reduce backend load and improve response latency for common queries.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Check cache for requested resource

2. Return cached data if valid

3. Fetch fresh data from backend if cache miss

4. Update cache with new response data

5. Set expiration time for cached entries


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Invalidate cache entries upon recipe updates

- Maintain cache consistency across distributed nodes

