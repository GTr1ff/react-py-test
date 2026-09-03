ROSETIC:90d0cbca-e11a-4eeb-bcef-4874dab8fbbe

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
**Faceted Filter Processor**

## Feature Description:
Aggregates search results into categories to enable efficient filtering by dietary tags, ingredients, and meal types.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Analyze the current result set for attribute distribution.

2. Calculate counts for each available facet category.

3. Apply active user filters to the result set.

4. Generate the updated facet count response.

5. Return the filtered results with facet metadata.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Facet counts must only include items matching the current query.

- Empty facets should be hidden from the response.

