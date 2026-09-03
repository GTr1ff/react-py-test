ROSETIC:4ab1f59d-5d2c-498f-9f4f-1bd5336a069e

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
**Tag Consistency Validator**

## Feature Description:
Ensures that all assigned tags remain valid and synchronized whenever the underlying taxonomy schema or recipe data undergoes modifications.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Monitor taxonomy schema change events.

2. Identify affected recipes linked to modified tags.

3. Re-evaluate tag validity against updated schema.

4. Update or remove invalid tags from recipe records.

5. Notify administrators of significant classification shifts.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Orphaned tags must be purged within 24 hours.

- System must maintain referential integrity between tags and recipes.

