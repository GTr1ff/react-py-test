ROSETIC:7d9ae2b5-bb95-4f04-b4a7-02d8194f5058

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
**Inventory Gap Analyzer**

## Feature Description:
Calculates the delta between required recipe ingredients and current pantry stock to determine missing items.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Extract ingredient requirements for eligible recipes.

2. Query current pantry inventory levels.

3. Calculate quantity differences for each ingredient.

4. Flag missing items and required purchase quantities.

5. Attach missing ingredient metadata to recipe objects.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Account for ingredient unit conversions.

- Ignore ingredients marked as pantry staples.

