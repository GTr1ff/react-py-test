ROSETIC:32d86854-64ce-4583-abe7-2321c0d34dc8

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
**Report Generation Scheduler**

## Feature Description:
Automates the creation and delivery of periodic summary reports for stakeholders based on predefined schedules.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Monitor schedule triggers for report generation

2. Execute batch queries for required metrics

3. Generate report document in PDF or CSV format

4. Upload generated file to secure storage bucket

5. Notify stakeholders via configured delivery channels


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Reports must be generated during off-peak hours

- Sensitive reports require encrypted storage

