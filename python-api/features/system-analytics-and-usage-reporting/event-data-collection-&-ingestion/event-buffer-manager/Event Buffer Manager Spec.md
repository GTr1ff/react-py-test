ROSETIC:a065fc00-d63b-4107-a366-f868a4fe18ee

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
**Event Buffer Manager**

## Feature Description:
Provides a durable, high-throughput message queue to decouple ingestion from downstream processing and prevent data loss.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Accept event batches from the ingestion gateway.

2. Write events to persistent distributed storage.

3. Acknowledge successful storage to the gateway.

4. Partition data streams for parallel processing.

5. Retain events until successful downstream consumption.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Events must be persisted before acknowledgment.

- Data retention period is set to seven days.

