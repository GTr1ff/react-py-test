ROSETIC:9711ff15-58f3-49dd-b607-b7f57fb0e109

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
**User Preference Profiler**

## Feature Description:
Aggregates historical interaction data to construct dynamic user interest vectors for recommendation model consumption.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch historical interaction logs from the data warehouse.

2. Calculate weighted scores for ingredient and recipe categories.

3. Normalize preference scores against global popularity metrics.

4. Store updated user interest vectors in the feature store.

5. Trigger model re-training events for updated profiles.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Profiles must be updated at least once every 24 hours.

- Inactive users older than 90 days are excluded from batch updates.

