ROSETIC:00f985d3-bd88-4d82-9c03-ab7b29c47d15

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
**Inventory State Transformer**

## Feature Description:
Converts raw database inventory records into a standardized schema optimized for consumption by the recommendation engine.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch current inventory records from the persistence layer.

2. Map raw ingredient attributes to the standardized recommendation schema.

3. Filter out items marked as depleted or expired.

4. Serialize the transformed data into a JSON payload.

5. Publish the payload to the recommendation engine integration endpoint.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Only active inventory items are included in the transformation.

- Standardized units must be used for all ingredient quantities.

