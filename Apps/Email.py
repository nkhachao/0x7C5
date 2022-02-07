from LongTermMemory import long_term_memory
from IntentClassifier import classify_op_intent
from DataTypes import DataTypes, Task


class EmailApp():
    def create_task(self, message):
        return Task('email', {})

    def process_task(self, task, message):
        title = task.data[DataTypes.Reminders_title]
        time = task.data[DataTypes.Time]
        date = task.data[DataTypes.Date]

        if not title:
            task.response = 'What should I remind you about?'
            return

        if not time and not date:
            task.response = 'When should I remind you this?'
            return

        if not time:
            datestring = ', ' + date
        elif not date:
            datestring = ', ' + time
        else:
            datestring = ', ' + time + ' ' + date

        long_term_memory.add_reminder({'Title': title, 'Time': datestring})
        task.complete()
        task.response = 'Ok. I\'ll remind you to ' + title + datestring + '.'
        return


class Reminder:
    title = None
    date = None