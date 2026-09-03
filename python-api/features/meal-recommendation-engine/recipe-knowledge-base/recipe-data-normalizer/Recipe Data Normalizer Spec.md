ROSETIC:54d7509f-605f-4ab4-97ad-a08ad213624a

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
**Recipe Data Normalizer**

## Feature Description:
Standardizes raw culinary data from diverse sources into a unified schema for consistent processing by the recommendation engine.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive raw recipe data from external sources.

2. Parse ingredient strings into structured entities.

3. Map units of measure to a standard system.

4. Validate nutritional data against defined ranges.

5. Persist normalized records to the master database.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All ingredients must map to a canonical master list.

- Nutritional values must be provided per serving.

