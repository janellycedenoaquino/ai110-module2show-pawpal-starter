# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:

1. **Add a pet** — enter basic owner and pet info to set up the system
2. **Add a care task** — log a task (e.g., walk, feeding, meds) with a duration and priority
3. **See today's schedule** — generate and view a prioritized daily plan

The initial UML design includes four classes:

- **Owner** — holds the owner's name, available hours for pet care, and a list of pets. Responsible for adding pets and providing access to all tasks across pets.
- **Pet** — holds the pet's name and species, and maintains a list of tasks. Responsible for adding and returning its own tasks.
- **Task** — represents a single care activity with a title, duration, priority, scheduled time, frequency, and completion status. Responsible for tracking and updating its own state via `mark_complete()`.
- **Scheduler** — holds a reference to the Owner and acts as the "brain" of the system. Responsible for retrieving all tasks, sorting by time, filtering, detecting conflicts, and generating the daily schedule.

**b. Design changes**

- Did your design change during implementation? Yes.
- If yes, describe at least one change and why you made it?
 During review of the class skeletons, one potential bottleneck was identified: both `Owner` and `Scheduler` define a `get_all_tasks()` method, which risks duplicating logic. To avoid this, `Scheduler.get_all_tasks()` will delegate directly to `owner.get_all_tasks()` rather than re-implementing the same traversal. This keeps task retrieval logic in one place and ensures the `Scheduler` stays focused on scheduling decisions rather than data access.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The method (`detect_conflicts`) uses a single-pass dictionary approach: it records the first task seen for each time slot and flags any later task that shares that same slot. So if three tasks are scheduled at the same time, it reports the first against the second and the first against the third — but not the second against the third directly.

This is a tradeoff is between simplicity and completeness. A full comparison would catch every conflict pair, but would require nested loops and produce redundant warnings. Since the goal is just to alert the owner that a time slot is overloaded. a single-pass approach is enough and keeps the code readable.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
