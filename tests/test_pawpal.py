from datetime import timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning Walk", duration=20, priority="high",
                scheduled_time="07:00", frequency="daily")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rocky", species="Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feeding", duration=10, priority="high",
                      scheduled_time="08:00", frequency="daily"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    pet.add_task(Task(title="Evening Walk", duration=30, priority="high", scheduled_time="18:00", frequency="daily"))
    pet.add_task(Task(title="Feeding",      duration=10, priority="high", scheduled_time="08:00", frequency="daily"))
    pet.add_task(Task(title="Morning Walk", duration=20, priority="high", scheduled_time="07:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.scheduled_time for t in sorted_tasks]
    assert times == ["07:00", "08:00", "18:00"]


def test_complete_task_creates_next_daily_occurrence():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    task = Task(title="Morning Walk", duration=20, priority="high", scheduled_time="07:00", frequency="daily")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task, pet_name="Rocky")
    assert task.is_complete == True
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert len(pet.get_tasks()) == 2


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    pet.add_task(Task(title="Walk",    duration=20, priority="high", scheduled_time="08:00", frequency="daily"))
    pet.add_task(Task(title="Feeding", duration=10, priority="high", scheduled_time="08:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


# --- Happy Path ---

def test_complete_task_creates_next_weekly_occurrence():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    task = Task(title="Bath Time", duration=30, priority="medium", scheduled_time="10:00", frequency="weekly")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task, pet_name="Rocky")
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(weeks=1)


# --- Edge Cases ---

def test_sort_by_time_with_no_tasks_returns_empty():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time() == []


def test_complete_nonrecurring_task_returns_none():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    task = Task(title="Vet Visit", duration=60, priority="high", scheduled_time="09:00", frequency="once")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    result = scheduler.complete_task(task, pet_name="Rocky")
    assert task.is_complete == True
    assert result is None
    assert len(pet.get_tasks()) == 1


def test_detect_conflicts_with_no_conflicts():
    owner = Owner(name="Nelly", available_hours=8)
    pet = Pet(name="Rocky", species="Dog")
    pet.add_task(Task(title="Walk",    duration=20, priority="high", scheduled_time="07:00", frequency="daily"))
    pet.add_task(Task(title="Feeding", duration=10, priority="high", scheduled_time="08:00", frequency="daily"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_with_no_tasks():
    owner = Owner(name="Nelly", available_hours=8)
    owner.add_pet(Pet(name="Rocky", species="Dog"))
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_owner_with_no_pets_returns_empty_schedule():
    owner = Owner(name="Nelly", available_hours=8)
    scheduler = Scheduler(owner)
    assert scheduler.generate_schedule() == []