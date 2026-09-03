ROSETIC:92d7147b-b01e-47bc-89ff-ffb0e36f6a96

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
**Relevance Ranking Engine**

## Feature Description:
Calculates the relevance score for search results based on metadata, popularity, and user-defined search criteria.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Retrieve candidate recipes matching the structured query.

2. Fetch popularity metrics for each candidate recipe.

3. Apply weighting factors to match quality and freshness.

4. Calculate final relevance scores for all candidates.

5. Sort results by the computed relevance score.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Recipes with missing nutritional data receive lower ranking.

- Exact title matches must be boosted in the final sort.

