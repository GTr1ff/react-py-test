ROSETIC:ddfde543-0bd6-418b-bd4e-08ff286699b6

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
**Dashboard Accessibility Provider**

## Feature Description:
Ensures that all dashboard components adhere to accessibility standards by providing semantic structure and screen reader support.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Inject ARIA labels into dynamic UI elements.

2. Validate keyboard navigation sequences for all interactive controls.

3. Apply high-contrast styling rules to visual indicators.

4. Generate descriptive text for non-text inventory status icons.

5. Verify compliance with WCAG standards during rendering.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- All interactive elements must be reachable via keyboard.

- Color-coded status indicators must have text-based alternatives.

