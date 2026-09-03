ROSETIC:70d549e8-168b-486e-9996-a67e6ac29d8a

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
**Request Authentication Service**

## Feature Description:
Validates incoming API requests by verifying credentials and tokens to ensure only authorized clients access the recipe data.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Intercept incoming API request

2. Extract authentication token from header

3. Verify token against identity provider

4. Validate client scope and permissions

5. Authorize request for downstream processing


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Reject requests with expired or invalid tokens

- Enforce least privilege access for all clients

