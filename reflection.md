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
  It considers the four following constraints:
  **time** (tasks are sorted chronologically by `scheduled_time`),
  **completion status** (tasks can be filtered by done vs. pending),
  **frequency** (daily and weekly tasks automatically recur using `timedelta`)
  **conflicts** (two tasks at the same time slot trigger a warning).

- How did you decide which constraints mattered most?

Time was treated as the primary constraint because a daily pet care schedule depends on the owner needs to know what to do and when. Priority is stored on each task and displayed in the UI, but the scheduler does not use it for ordering. This was a deliberate simplicity choice given the scope of the project.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The method (`detect_conflicts`) uses a single-pass dictionary approach: it records the first task seen for each time slot and flags any later task that shares that same slot. So if three tasks are scheduled at the same time, it reports the first against the second and the first against the third — but not the second against the third directly.

This is a tradeoff is between simplicity and completeness. A full comparison would catch every conflict pair, but would require nested loops and produce redundant warnings. Since the goal is just to alert the owner that a time slot is overloaded. a single-pass approach is enough and keeps the code readable.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  AI was used across every phase of the project. During the design, it helped generate the initial Mermaid UML diagram and class skeletons from brainstormed attributes and methods.
  During implementation, Agent/Edit mode was used to create the `Scheduler` methods like `sort_by_time`, `filter_tasks`, `detect_conflicts`, and `complete_task`.

During testing, AI drafted test functions for both happy paths and edge cases even though it repeated alot of the code. after being asked about the most important behaviors to verify. For documentation, AI generated docstrings for all methods and helped draft README sections like "Features" and "Smarter Scheduling."

The most effective claude features were **Agent Mode** for multi-method implementation in one pass, **Inline Chat** for targeted questions on specific lines, **Generate Tests** for drafting the test suite, **Generate Documentation** for adding docstrings quickly, and **`#codebase` / `#file:` references** for giving the AI enough context to produce accurate, relevant responses.

- What kinds of prompts or questions were most helpful?
  The most helpful prompts were ones that referenced specific files (e.g., `#file:pawpal_system.py`) to give the AI enough context for accurate, relevant answers.
  Asking "how should X talk to Y?" helped clarify relationships between classes — for example, how `Scheduler` should retrieve tasks from `Owner`. Asking "what are the most important edge cases to test for a pet scheduler?" produced a structured list that directly guided the test suite. Using separate chat sessions per phase also helped — keeping design, implementation, algorithms, and testing conversations separate prevented earlier context from bleeding into later phases, making it easier to evaluate whether a suggestion fit the current goal or was out of scope.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  Several times during the project, AI suggested adding features that were not part of the requirements — such as additional scheduling capabilities or UI enhancements that would have significantly expanded the scope. Rather than accepting these, I did not accept changes and explained what was actually needed for the project and to only implement what was asked.

- How did you evaluate or verify what the AI suggested?
  The evaluation was straightforward: if a suggestion wasn't listed in the project instructions, it was set aside. This kept the codebase focused and the implementation manageable. It was a good reminder that AI tends to suggest improvements and extensions by default, and that the I have to read and make sure to keep the project on track. Being the "lead architect" meant that every AI suggestion was a proposal, not a decision — the finnal call on what to keep, reject, or simplify always came from reviewing the project requirements and making sure the design stayed coherent.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  The test covered 11 behaviors:
  - task completion (`mark_complete()` updates status)
  - task addition (pet task count increases)
  - sorting correctness (tasks returned in chronological order regardless of insertion order)
  - daily recurrence (completing a daily task creates a new one for the next day)
  - weekly recurrence (completing a weekly task creates one 7 days later)
  - conflict detection (duplicate time slots are flagged).
  - Edge cases were also tested:
    - a pet with no tasks
    - completing a non-recurring task (returns `None`)
    - a schedule with no conflicts
    - an empty task list
    - an owner with no pets.

- Why were these tests important?
  These behaviors are the core part of the app— if sorting, recurrence, or conflict detection is broken, the entire schedule is unreliable. Testing them in isolation made it easy to catch logic bugs before they surfaced in the UI and gave confidence that the `Scheduler` class works correctly regardless of how it's called.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  Confidence: 4 out of 5 stars. All 11 tests pass and cover the core behaviors and key edge cases. The scheduler is reliable for the expected use cases — adding pets, scheduling tasks, sorting, filtering, detecting conflicts, and recurring tasks all work as designed.

- What edge cases would you test next if you had more time?
  Edge cases to test next with more time:
  - Invalid time format input (e.g., `"25:00"` or `"abc"`) — `sort_by_time()` would crash because `datetime.strptime` would throw an error
  - Marking a task complete that is already complete — currently allowed without any guard
  - Two pets with the exact same name — `filter_tasks(pet=...)` would return tasks from both, which may not be the intended behavior
  - A very large number of tasks — no performance testing has been done on the sorting or conflict detection methods

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The most satisfying part of the project was learning how to collaborate with AI effectively — asking focused, context-rich questions and knowing when to accept or push back on suggestions. Using file references and phase-specific chat sessions made the AI responses much more useful and kept the work organized. The final look of the Streamlit app was also a highlight — seeing the logic layer connect cleanly to a polished UI made the whole system feel complete.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Four things:
First, data persistence — everything currently lives in `st.session_state`, which means refreshing the page wipes all pets and tasks. Adding save/load functionality (e.g., to a JSON file) would make the app genuinely useful day-to-day rather than just a demo.
Second, duplicate pet names — the app doesn't prevent two pets from having the same name, which would cause `filter_tasks(pet=...)` to return tasks from both pets unintentionally. Adding a uniqueness check when adding a pet would be a small fix with a big impact on reliability.
Third, owner name validation — the app currently allows a pet to be added without the owner first entering their name. Adding a guard that requires the owner name field to be filled before any pets or tasks can be added would make the flow more intentional and prevent orphaned data.
Fourth, task deletion — once a task is added there is no way to remove it. Adding a delete button or checkbox next to each task in the table would give the owner control over their schedule and make the app significantly more practical to use.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Two takeaways from this project are first that, AI needs direction — it's only as useful as the questions you ask it. Without clear, specific prompts it either over-engineers or suggests features that are out of scope and Second that, designing first saves time — starting with a UML diagram before writing any code gave the implementation phase a clear roadmap, and skipping that step would have led to unnecessary refactoring later and probably adding features you shouldn't for MVP.
