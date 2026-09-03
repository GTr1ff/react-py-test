ROSETIC:96d0164f-9eef-42b5-b62f-3de0a32dd356

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
**Data Subject Request Processor**

## Feature Description:
Automates the workflow for handling user requests regarding data access, portability, and permanent deletion.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive formal data deletion or export request.

2. Verify user identity against authentication provider.

3. Trigger cascading deletion jobs across all data stores.

4. Generate confirmation report upon completion.

5. Notify user of request status via secure channel.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Deletion requests must be fulfilled within the legally mandated timeframe.

- All data deletion actions must be logged for compliance auditing.

