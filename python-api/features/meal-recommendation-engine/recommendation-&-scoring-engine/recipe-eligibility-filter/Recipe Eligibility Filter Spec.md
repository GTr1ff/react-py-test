ROSETIC:7b939876-6652-49f3-b67c-df0f39ef4bd4

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
**Recipe Eligibility Filter**

## Feature Description:
Evaluates raw recipe data against user dietary profiles to exclude incompatible options before the scoring phase.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch user dietary restrictions and allergy data.

2. Retrieve candidate recipes from the knowledge base.

3. Compare recipe ingredients against restricted lists.

4. Discard recipes containing prohibited allergens.

5. Pass eligible recipe IDs to the scoring service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Exclude recipes containing flagged allergens.

- Respect strict dietary exclusion rules.

