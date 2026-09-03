ROSETIC:0305b71e-afa7-4030-b00b-de50aaea411a

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
**Skill Level Adaptation Engine**

## Feature Description:
Adjusts recipe recommendations by matching recipe complexity metadata against the user's documented culinary skill level.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch user skill level classification.

2. Retrieve complexity metadata for candidate recipes.

3. Compare recipe difficulty against user skill.

4. Apply penalty scores to overly complex recipes.

5. Filter out recipes exceeding user skill threshold.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Users can opt-out of skill-based filtering.

- Recipes without complexity metadata are treated as medium difficulty.

