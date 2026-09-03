ROSETIC:bfb50570-20e6-4cf2-aaa2-63fc68a1cc47

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
**Recommendation Result Formatter**

## Feature Description:
Packages ranked recipe results with supporting metadata for consumption by the application interface.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive sorted recipe list from the orchestrator.

2. Aggregate recipe details and missing item lists.

3. Format data into standardized JSON response structures.

4. Attach confidence scores to each recommendation.

5. Publish final recommendation set to the output queue.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Limit result set to top ten recommendations.

- Include reasoning metadata for top-ranked items.

