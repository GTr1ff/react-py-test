ROSETIC:1acebd2e-6a77-4f67-b044-f79898564ee4

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
**Recommendation Model Orchestrator**

## Feature Description:
Manages the execution of multiple recommendation algorithms to generate candidate recipe sets for specific user segments.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive request for personalized recipe recommendations.

2. Select appropriate algorithm based on user profile maturity.

3. Execute collaborative filtering and content-based logic.

4. Merge candidate lists from multiple algorithm outputs.

5. Rank candidates using a secondary scoring function.

6. Return top-N recipe identifiers to the requesting service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Cold-start users receive popular recipes instead of personalized ones.

- Maximum latency for recommendation generation is 200 milliseconds.

