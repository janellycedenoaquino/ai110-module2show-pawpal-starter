from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Nelly", available_hours=8)

rocky = Pet(name="Rocky", species="Dog")
bill = Pet(name="Billie", species="Dog")
tommy = Pet(name="Tommy", species="Cat")

# --- Add tasks OUT OF ORDER intentionally ---
rocky.add_task(Task(title="Evening Walk",   duration=30, priority="high",   scheduled_time="18:00", frequency="daily"))
rocky.add_task(Task(title="Fish Oil Treats", duration=5,  priority="medium", scheduled_time="08:00", frequency="weekly"))
rocky.add_task(Task(title="Morning Walk",   duration=20, priority="high",   scheduled_time="07:00", frequency="daily"))

tommy.add_task(Task(title="Playtime",       duration=15, priority="low",    scheduled_time="17:00", frequency="daily"))
tommy.add_task(Task(title="Feeding",        duration=10, priority="high",   scheduled_time="9:00",  frequency="daily"))

bill.add_task(Task(title="Fish Oil Treats", duration=5,  priority="medium", scheduled_time="08:00", frequency="weekly"))
bill.add_task(Task(title="Evening Walk",    duration=30, priority="high",   scheduled_time="18:00", frequency="daily"))
bill.add_task(Task(title="Morning Walk",    duration=20, priority="high",   scheduled_time="07:00", frequency="daily"))

# --- Register pets with owner ---
owner.add_pet(rocky)
owner.add_pet(tommy)
owner.add_pet(bill)

# --- Scheduler ---
scheduler = Scheduler(owner)

# --- Conflict check ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("⚠️  Conflicts detected:")
    for warning in conflicts:
        print(f"   {warning}")
    print()

# --- Test: sort_by_time ---
print("=" * 40)
print("   🕐 All Tasks Sorted by Time")
print("=" * 40)
for task in scheduler.sort_by_time():
    print(f"  {task.scheduled_time}  {task.title:<20} ({task.priority})")
print()

# --- Test: filter_tasks by pet name ---
print("=" * 40)
print("   🐕 Rocky's Tasks Only")
print("=" * 40)
for task in scheduler.filter_tasks(pet="Rocky"):
    status = "✓" if task.is_complete else "○"
    print(f"  [{status}] {task.scheduled_time}  {task.title:<20} {task.duration} min")
print()

# --- Mark one task complete for status filter demo ---
rocky_tasks = scheduler.filter_tasks(pet="Rocky")
rocky_tasks[0].mark_complete()

# --- Test: filter_tasks by completion status ---
print("=" * 40)
print("   ✓  Completed Tasks")
print("=" * 40)
completed = scheduler.filter_tasks(status=True)
if completed:
    for task in completed:
        print(f"  ✓ {task.scheduled_time}  {task.title:<20}")
else:
    print("  None yet.")
print()

print("=" * 40)
print("   ○  Incomplete Tasks")
print("=" * 40)
for task in scheduler.filter_tasks(status=False):
    print(f"  ○ {task.scheduled_time}  {task.title:<20} ({task.priority})")
print("=" * 40)
print()

# --- Test: recurring task ---
rocky_tasks = scheduler.filter_tasks(pet="Rocky")
morning_walk = next(t for t in rocky_tasks if t.title == "Morning Walk")
print("=" * 40)
print("   🔁 Recurring Task Demo")
print("=" * 40)
print(f"  Completing '{morning_walk.title}' scheduled for {morning_walk.due_date} ...")
next_task = scheduler.complete_task(morning_walk, pet_name="Rocky")
print(f"  ✓ Marked complete.")
if next_task:
    print(f"  ↺ Next occurrence created: '{next_task.title}' on {next_task.due_date}")
print("=" * 40)
