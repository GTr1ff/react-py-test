ROSETIC:ae5ebc3d-bf18-4db9-94c9-2c67b81b692a

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
**Recommendation Feedback Loop**

## Feature Description:
Captures and processes user interactions with recommended items to refine future model accuracy.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Listen for recommendation impression and click events.

2. Correlate events with the specific recommendation session ID.

3. Update reward signals for the underlying recommendation model.

4. Log feedback data for offline model performance evaluation.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Click-through rate must be tracked per recommendation algorithm.

- Feedback data must be anonymized before storage in the training set.

