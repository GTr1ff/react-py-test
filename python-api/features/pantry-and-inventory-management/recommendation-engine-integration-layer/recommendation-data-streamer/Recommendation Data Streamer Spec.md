ROSETIC:2ef03a03-4a1b-4722-b25a-b83de0dea797

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
**Recommendation Data Streamer**

## Feature Description:
Manages asynchronous data streams to push inventory updates to the recommendation engine in real-time.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Subscribe to inventory change events from the core system.

2. Buffer incoming change events for batch processing.

3. Aggregate multiple updates into a single synchronization message.

4. Transmit the aggregated message to the recommendation engine queue.

5. Acknowledge successful delivery of the data stream.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Data streams must maintain strict ordering of inventory updates.

- Failed transmissions require a retry mechanism with exponential backoff.

