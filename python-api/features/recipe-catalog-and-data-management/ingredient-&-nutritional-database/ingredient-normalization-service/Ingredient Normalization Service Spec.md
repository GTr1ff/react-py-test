ROSETIC:2d964f71-fc2b-4bf9-ac70-42fe993f9c04

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
**Ingredient Normalization Service**

## Feature Description:
Standardizes raw ingredient inputs into a unified schema to ensure consistency across the entire recipe catalog.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive raw ingredient data from ingestion sources.

2. Match input against the master ingredient registry.

3. Map non-standard units to system-defined measurements.

4. Validate ingredient attributes against schema constraints.

5. Persist normalized records to the primary database.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All ingredients must map to a unique system identifier.

- Unit conversions must follow defined SI or culinary standards.

