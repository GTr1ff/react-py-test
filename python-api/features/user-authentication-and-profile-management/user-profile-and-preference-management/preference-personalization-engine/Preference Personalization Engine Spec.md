ROSETIC:7687db06-364f-496a-b901-75d1352ccc8a

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
**Preference Personalization Engine**

## Feature Description:
Aggregates and transforms raw culinary preferences into structured profiles used by recommendation services to tailor content.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch raw preference data from profile store.

2. Apply weighting algorithms to preference attributes.

3. Generate optimized preference vector for user.

4. Cache vector for low-latency retrieval.

5. Publish update event to recommendation service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Preference vectors must be updated on every profile change.

- Cache TTL must not exceed five minutes.

