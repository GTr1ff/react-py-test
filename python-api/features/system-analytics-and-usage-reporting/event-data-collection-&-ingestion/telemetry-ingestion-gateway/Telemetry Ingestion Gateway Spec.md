ROSETIC:a3b3180c-16c7-42bd-adcc-c838559e1b9e

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
**Telemetry Ingestion Gateway**

## Feature Description:
Acts as the primary entry point for high-throughput event traffic, providing load balancing and initial request authentication.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive incoming HTTP requests from client applications.

2. Authenticate request origin and session tokens.

3. Rate-limit traffic to protect downstream services.

4. Forward validated payloads to the message broker.

5. Return acknowledgment status to the client.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Requests must contain valid authentication headers.

- Traffic exceeding defined thresholds is throttled.

