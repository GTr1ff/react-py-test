ROSETIC:8f597214-f377-4a3c-9a37-58ac0a4e8537

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
**Data Retention and Archival Manager**

## Feature Description:
Manages the lifecycle of stored event data by moving aged records to cold storage to optimize warehouse costs.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Scan data partitions for records exceeding retention limits.

2. Compress identified datasets for long-term storage.

3. Move compressed files to low-cost object storage.

4. Delete expired records from the primary warehouse.

5. Update metadata catalog with new storage locations.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Retain raw event data for exactly three years.

- Ensure data integrity during migration processes.

