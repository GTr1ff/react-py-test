ROSETIC:d5cc84a3-6291-4f19-a69e-78093f735178

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
**Query Parser and Normalizer**

## Feature Description:
Translates raw search queries into structured search parameters to ensure consistent execution across the search engine.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Receive raw search query strings from the API gateway.

2. Sanitize input to prevent injection attacks.

3. Tokenize query terms into searchable keywords.

4. Map keywords to known taxonomy and ingredient categories.

5. Construct a structured query object for the search engine.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Queries must be normalized to lowercase before processing.

- Stop words must be removed from search tokens.

