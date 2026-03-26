# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest 
```
or for mac
```
python3 -m pytest
```

The tests cover:

- **Task completion** — verifies `mark_complete()` correctly updates the task's status
- **Task addition** — verifies adding a task to a pet increases that pet's task count
- **Sorting correctness** — verifies tasks are returned in chronological order regardless of insertion order
- **Recurrence logic** — verifies that completing a daily task creates a new task for the next day, and a weekly task creates one 7 days later
- **Conflict detection** — verifies the scheduler flags two tasks scheduled at the same time
- **Edge cases** — covers pet with no tasks, non-recurring task completion, no conflicts, empty task list, and owner with no pets

Confidence: ⭐⭐⭐⭐ — all core behaviors and key edge cases are verified; the system behaves reliably for the expected use cases.

---

## Smarter Scheduling

PawPal+ goes beyond a basic task list with the following algorithmic features:

- **Sort by time** — tasks are automatically sorted chronologically so the daily schedule is always in order, regardless of the order they were added
- **Filter tasks** — tasks can be filtered by pet name or completion status to quickly see what's done and what's pending
- **Conflict detection** — the scheduler scans all tasks across all pets and warns the owner when two tasks are scheduled at the same time
- **Recurring tasks** — when a `daily` or `weekly` task is marked complete, a new instance is automatically created for the next occurrence using Python's `timedelta`

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
