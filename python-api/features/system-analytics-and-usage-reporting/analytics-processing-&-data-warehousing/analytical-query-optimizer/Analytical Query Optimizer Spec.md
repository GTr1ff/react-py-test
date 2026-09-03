ROSETIC:3ae5a8ca-4805-4fb2-8ec1-cad98e7053c6

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
**Analytical Query Optimizer**

## Feature Description:
Maintains indexing strategies and partitioning schemes to ensure high-performance execution of complex analytical queries.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Analyze query patterns from the reporting dashboard.

2. Identify frequently accessed data dimensions.

3. Rebuild indexes on high-traffic table columns.

4. Adjust table partitioning based on temporal trends.

5. Monitor query execution times for performance regressions.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Prioritize index updates for top-ten queries.

- Minimize storage overhead during re-indexing.

