class DataTypes:
    Reminders_title = 'REMINDERS'
    Date = 'DATE'
    Time = 'TIME'


class Task:
    def __init__(self, app, data):
        self.id = None
        self.app = app
        self.data = data
        self.is_active = True
        self.is_completed = False
        self.is_cancelled = False
        self.priority = 0
        self.response = ''

    def processing(self):
        self.is_active = True

    def complete(self):
        self.is_active = False
        self.is_completed = True
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True
        self.is_completed = False
        self.is_active = False

    def empty_slots(self):
        result = []
        for key, value in self.data.items():
            if value is None:
                result.append(key)

        return result

    def fill(self, field, data):
        self.data[field] = data