ROSETIC:fc7abf2a-433a-4322-a8a7-72308f288a68

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
**Inventory Persistence Service**

## Feature Description:
Manages the primary storage and retrieval of inventory records within the database to ensure data integrity and availability.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive write requests for inventory records.

2. Validate schema compliance of incoming data.

3. Execute database transaction for record persistence.

4. Confirm successful commit to the calling service.

5. Log transaction details for audit purposes.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All inventory records must have a unique identifier.

- Database transactions must maintain ACID compliance.

