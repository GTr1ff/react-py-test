ROSETIC:e6a09910-d4ed-4df8-8008-42c5ccb63adf

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
Maintains a tamper-proof record of all data access and processing activities for regulatory reporting and internal auditing.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Capture access logs from data storage services.

2. Enrich logs with metadata and request context.

3. Sign log entries with cryptographic timestamps.

4. Archive logs to write-once-read-many storage.

5. Generate periodic compliance reports for stakeholders.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Audit logs must be retained for a minimum of seven years.

- Unauthorized modification of audit logs must trigger an immediate security alert.

