ROSETIC:feaab7f8-6d19-4035-a487-a9e072c30e55

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
**Data Aggregation Engine**

## Feature Description:
Performs batch processing to compute daily and weekly KPIs from normalized event logs for analytical consumption.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Trigger scheduled aggregation jobs for specific time windows.

2. Query normalized event data from the staging area.

3. Calculate ingredient popularity and meal frequency metrics.

4. Write aggregated results to the analytical data warehouse.

5. Update materialized views for reporting performance.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Execute aggregations during off-peak hours.

- Ensure idempotent processing of event batches.

