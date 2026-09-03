ROSETIC:8b341064-1ad0-41fc-b94e-d350a4159e36

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
**Visualization Data Transformer**

## Feature Description:
Converts raw analytical result sets into structured formats required by frontend charting libraries.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch raw data from query execution engine

2. Apply requested aggregation or grouping logic

3. Map data points to chart-specific schema

4. Inject metadata for axis labels and legends

5. Serialize output into JSON response payload


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Data must be normalized before visualization

- Empty datasets must return standardized null structures

