ROSETIC:7d240137-b953-4f7f-8372-0c48a33f9f79

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
**Notification Dispatcher**

## Feature Description:
Routes expiration alerts to appropriate communication channels based on user-defined notification settings.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive expiration event from the message bus.

2. Retrieve user notification preferences from profile service.

3. Format alert message based on ingredient urgency.

4. Dispatch notification to configured delivery endpoints.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Notifications must respect user-defined quiet hours.

- Duplicate alerts for the same item are suppressed within 24 hours.

