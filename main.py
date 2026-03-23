from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Nelly", available_hours=8)

rocky = Pet(name="Rocky", species="Dog")
bill = Pet(name="Billie", species="Dog")
tommy = Pet(name="Tommy", species="tommy" )

# --- Add tasks to Rocky (out of order intentionally) ---
rocky.add_task(Task(title="Evening Walk",    duration=30, priority="high",   scheduled_time="18:00", frequency="daily"))
rocky.add_task(Task(title="Morning Walk",    duration=20, priority="high",   scheduled_time="07:00", frequency="daily"))
rocky.add_task(Task(title="Fish Oil Treats",  duration=5,  priority="medium", scheduled_time="08:00", frequency="weekly"))

# --- Add tasks to Tommy ---
tommy.add_task(Task(title="Feeding",         duration=10, priority="high",   scheduled_time="08:00", frequency="daily"))
tommy.add_task(Task(title="Playtime",        duration=15, priority="low",    scheduled_time="17:00", frequency="daily"))

# --- Add tasks to bill ---
bill.add_task(Task(title="Evening Walk",    duration=30, priority="high",   scheduled_time="18:00", frequency="daily"))
bill.add_task(Task(title="Morning Walk",    duration=20, priority="high",   scheduled_time="07:00", frequency="daily"))
bill.add_task(Task(title="Fish Oil Treats",  duration=5,  priority="medium", scheduled_time="08:00", frequency="weekly"))

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

# --- Today's Schedule ---
schedule = scheduler.generate_schedule()

print("=" * 40)
print("        🐾 Today's Schedule")
print("=" * 40)
for task in schedule:
    status = "✓" if task.is_complete else "○"
    print(f"  [{status}] {task.scheduled_time}  {task.title:<20} {task.duration} min  ({task.priority})")
print("=" * 40)