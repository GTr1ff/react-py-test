ROSETIC:5885c535-7fc5-4586-a2b4-6260db8af183

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
**Heuristic Scoring Orchestrator**

## Feature Description:
Applies weighted algorithms to rank recipes based on inventory utilization, nutritional targets, and user preference alignment.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive filtered recipes and gap analysis data.

2. Calculate utilization score based on pantry usage.

3. Compute nutritional alignment against user goals.

4. Apply preference weights to final scores.

5. Sort recipes by descending heuristic value.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Prioritize recipes minimizing new purchases.

- Weight nutritional balance by user profile settings.

