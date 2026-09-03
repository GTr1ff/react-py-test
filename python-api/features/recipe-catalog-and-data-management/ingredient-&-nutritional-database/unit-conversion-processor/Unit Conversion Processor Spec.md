ROSETIC:37a3aa14-5d90-4549-8161-7a1f4f2a783f

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
**Unit Conversion Processor**

## Feature Description:
Provides automated conversion logic between different units of measure for ingredient quantities.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive conversion request with source and target units.

2. Lookup conversion factor in the unit registry.

3. Perform mathematical transformation on the quantity value.

4. Return the converted value to the requesting service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Conversion factors must be defined for all supported units.

- Precision loss must be minimized during floating-point operations.

