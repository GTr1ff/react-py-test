ROSETIC:b314f9f7-9727-464e-ac57-c2affd063c43

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
**Search Indexer Service**

## Feature Description:
Maintains the high-performance search index by synchronizing recipe data from the primary database into a searchable format.

---

## Objective
Read all the information that you have, as well as the codebase (if available), before implementing the feature. 
Understand what features or functionalities are or should already be available in the system and reuse them if applicable.
Implement the described feature end-to-end based on the provided steps and rules.
If not already available, you may design supporting components (e.g., APIs, services, data models, or utility modules) as necessary, ensuring clarity and modularity.

---

## Implementation Steps
*(Follow these in sequence. Do not modify their content.)*


1. Listen for recipe update events from the message bus.

2. Fetch full recipe details from the primary database.

3. Transform recipe data into a flattened search document.

4. Update the search index with the new document.

5. Verify index consistency against the source record.


---

## Rules & Constraints
*(These must always be satisfied. Do not alter their wording.)*


- Index updates must occur within five seconds of data changes.

- Failed indexing attempts must trigger a retry mechanism.

