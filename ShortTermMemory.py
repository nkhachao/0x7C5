import random

class ShortTermMemory:
    def __init__(self):
        self.tasks = {}
        self.conversation = []

    def add_task(self, task):
        if task:
            taken_ids = self.tasks.keys()
            new_id = random.randint(0, 128)
            while new_id in taken_ids:
                new_id = random.randint(0, 128)

            task.id = new_id
            self.tasks[new_id] = task

    def update_task(self, task):
        self.tasks[task.id] = task

    def processing_tasks(self):
        results = list(filter(lambda x: x.is_active, self.tasks.values()))

        def prioritize(val):
            return val.priority

        results.sort(key = prioritize)
        return results


short_term_memory = ShortTermMemory()