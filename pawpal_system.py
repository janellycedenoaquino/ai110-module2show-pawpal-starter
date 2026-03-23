from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration: int
    priority: str
    scheduled_time: str
    frequency: str
    is_complete: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_hours: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        pass

    def sort_by_time(self) -> List[Task]:
        pass

    def filter_tasks(self, pet: str = None, status: bool = None) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[str]:
        pass

    def generate_schedule(self) -> List[Task]:
        pass
