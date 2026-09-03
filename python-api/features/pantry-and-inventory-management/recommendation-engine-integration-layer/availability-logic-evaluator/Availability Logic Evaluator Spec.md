ROSETIC:77365eee-b1d6-41f5-9bdd-bda0ee0381de

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
**Availability Logic Evaluator**

## Feature Description:
Determines the real-time availability status of ingredients based on quantity thresholds and expiration status.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive a request for ingredient availability status.

2. Query current quantity levels for requested ingredients.

3. Compare quantities against defined minimum threshold values.

4. Evaluate expiration dates against the current system date.

5. Return a boolean availability flag for each ingredient.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Ingredients with zero quantity are marked as unavailable.

- Ingredients past their expiration date are marked as unavailable.

