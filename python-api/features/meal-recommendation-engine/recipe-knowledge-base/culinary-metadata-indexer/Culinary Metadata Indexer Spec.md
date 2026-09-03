ROSETIC:dd2d12fa-beca-4696-af75-1ba8ac9723fe

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
**Culinary Metadata Indexer**

## Feature Description:
Maintains searchable indices for recipe attributes to enable high-performance filtering and retrieval by the recommendation engine.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Detect updates to recipe metadata records.

2. Extract tags and dietary classification attributes.

3. Update inverted indices for fast lookup.

4. Refresh search cache for active recipe queries.

5. Broadcast index update events to downstream services.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Indices must reflect changes within five seconds.

- Dietary tags must follow a strict taxonomy.

