ROSETIC:5a417f25-e48a-481d-8128-2cdd3c157703

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
**Data Transformation Engine**

## Feature Description:
Converts internal recipe data models into external-facing formats to maintain schema decoupling between internal storage and client consumption.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Fetch raw data from internal services

2. Map internal fields to public schema

3. Filter sensitive internal metadata fields

4. Serialize data into requested output format

5. Attach standard response headers


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Strip internal database IDs from public responses

- Ensure consistent unit conversion for all ingredients

