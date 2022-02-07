from Tagger import pos_tag, ner_tag, reminders_tag
from LongTermMemory import long_term_memory
from IntentClassifier import classify
from DataTypes import DataTypes, Task
from Answerer import query_table, query_passage, single_query_table


class QuestionAnsweringApp():
    def create_task(self, message):
        task = Task('question answering', {})

        return task

    def process_task(self, task, message):
        intent = classify(message, ['Question about schedules and reminders', 'Question about contacts'])
        task.response = 'I don\'t know anything about this, sorry.'

        data = None
        if intent == 'Question about schedules and reminders':
            data = single_query_table(long_term_memory.reminders, message)
        elif intent == 'Question about contacts':
            data = single_query_table(long_term_memory.contacts, message)

        if data:
            task.response = ', '.join(data) + '.'

        task.complete()
        return


class Reminder:
    title = None
    date = None