ROSETIC:9ac9d57e-2251-41fb-af5f-f319e38fc372

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
**Compliance Audit Logger**

## Feature Description:
Records all privacy-related events to ensure traceability and regulatory compliance reporting.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Capture privacy event metadata from system services.

2. Sanitize event data for sensitive information.

3. Write event log to immutable storage.

4. Generate periodic compliance summary reports.

5. Alert administrators on unauthorized data access attempts.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Audit logs must be retained for a minimum of seven years.

- Logs must be digitally signed to prevent tampering.

