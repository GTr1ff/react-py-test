ROSETIC:3d8d32b1-d7c4-4037-add0-20cf1c7b5869

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
**Inventory View Aggregator**

## Feature Description:
Consolidates raw inventory data and metadata into a unified view model for efficient rendering on the dashboard.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch current inventory records from the persistence service.

2. Retrieve associated metadata for each inventory item.

3. Merge inventory status with category and unit information.

4. Format the aggregated data into a structured JSON response.

5. Cache the final view model for rapid dashboard retrieval.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Only active inventory items are included in the aggregation.

- Data must be sorted by expiration date by default.

