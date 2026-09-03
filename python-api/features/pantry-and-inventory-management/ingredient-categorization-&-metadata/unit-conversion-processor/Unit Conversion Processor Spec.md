ROSETIC:26888659-9865-4abe-985f-fd107a51aa13

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
Normalizes disparate measurement units into a standard internal format for accurate inventory calculation and recipe matching.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive ingredient quantity and unit type.

2. Lookup conversion factor for the specified unit.

3. Calculate normalized value in base system units.

4. Store normalized value alongside original input.

5. Return conversion confirmation to the calling service.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Conversion factors must be defined for all supported units.

- Rounding must occur to the nearest two decimal places.

