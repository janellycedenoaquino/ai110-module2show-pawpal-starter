from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration: int
    priority: str
    scheduled_time: str
    frequency: str
    is_complete: bool = False

    def mark_complete(self):
        """Mark this task as complete."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_hours: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by scheduled time."""
        return sorted(self.get_all_tasks(), key=lambda t: t.scheduled_time)

    def filter_tasks(self, pet: Optional[str] = None, status: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.get_all_tasks()
        if pet is not None:
            tasks = []
            for p in self.owner.pets:
                if p.name == pet:
                    tasks = p.get_tasks()
        if status is not None:
            tasks = [t for t in tasks if t.is_complete == status]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any tasks scheduled at the same time."""
        tasks = self.get_all_tasks()
        seen_times = {}
        warnings = []
        for task in tasks:
            if task.scheduled_time in seen_times:
                warnings.append(
                    f"Conflict at {task.scheduled_time}: '{seen_times[task.scheduled_time]}' and '{task.title}'"
                )
            else:
                seen_times[task.scheduled_time] = task.title
        return warnings

    def generate_schedule(self) -> List[Task]:
        """Generate a daily schedule by returning all tasks sorted by time."""
        return self.sort_by_time()