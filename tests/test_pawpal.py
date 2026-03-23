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