from BERT import embed
from IntentClassifier import classify_intent
from Tagger import pos_tag, ner_tag, reminders_tag
from LongTermMemory import long_term_memory, LongTermMemory
from ShortTermMemory import short_term_memory, ShortTermMemory
from Apps.Reminders import ReminderApp
from Apps.Memorization import MemorizationApp
from Apps.Email import EmailApp
from Apps.QuestionAnswering import QuestionAnsweringApp
from DataTypes import DataTypes, Task


class Assistant:
    def __init__(self):
        self.apps = {'reminders': ReminderApp(), 'memorization': MemorizationApp(), 'question answering': QuestionAnsweringApp(), 'email': EmailApp()}

    def respond(self, message):
        response = []
        tasks = short_term_memory.processing_tasks()
        if tasks:
            response += self.process_tasks(message)
        else:
            intents = classify_intent(message)

            if 'information retrieve' in intents:       # Do not learn from questions
                app = self.apps['question answering']
                task = app.create_task(message)
                short_term_memory.add_task(task)

            else:
                app = self.apps.get(intents[0], None)

                if app:
                    task = app.create_task(message)
                    short_term_memory.add_task(task)

                    if 'requires task confirmation' in intents and task and not task.is_cancelled:
                        response.append('Sure.')

                app = self.apps['memorization']
                task = app.create_task(message)

                if task:
                    task.priority = -1
                    short_term_memory.add_task(task)

                response += self.process_tasks(message)

        response = ' '.join(response)
        if response:
            return response[0].upper() + response[1:]
        else:
            return 'I have nothing to say...'

    def process_tasks(self, message):
        response = []
        tasks = short_term_memory.processing_tasks()

        if tasks:
            task = tasks[-1]
            response.append(self.process_task(task, message))
            if task.is_completed:
                tasks = short_term_memory.processing_tasks()
                if tasks:
                    task = tasks[-1]
                    if task.response:
                        response += task.response

        return response

    def process_task(self, task, message):
        app = None
        response = ''
        app = self.apps[task.app]

        response += self.fill_data(task, message)

        app.process_task(task, message)
        response += task.response
        task.response = ''

        short_term_memory.update_task(task)
        return response

    def fill_data(self, task, message):
        response = ''
        for field in task.empty_slots():
            data = self.extract(message, field)
            if data:
                task.fill(field, data)
                response += ('' if not response else ', ') + data

        if response:
            return response + '. '
        else:
            return ''

    def extract(self, message, data_type):
        if data_type == DataTypes.Reminders_title:
            result = reminders_tag(message)
            if result:
                return result

        if data_type == DataTypes.Date:
            result = ''
            for text, tag in ner_tag(message):
                if tag == 'DATE':
                    result += text

            if result:
                return result

        if data_type == DataTypes.Time:
            result = ''
            for text, tag in ner_tag(message):
                if tag == 'TIME':
                    result += text

            if result:
                return result


assistant = Assistant()


if __name__ == "__main__":
    def start_conversation(allow_multiple_sentences):
        utterance = ''

        while True:
            message = input("> ")

            if message == 'RESET':
                global short_term_memory
                global long_term_memory

                short_term_memory = ShortTermMemory()
                long_term_memory = LongTermMemory()
                continue

            if utterance == '':
                utterance = message
            elif utterance[-1] == '?':
                utterance += (' ' + message)
            else:
                utterance += ('. ' + message)

            if message == '' or not allow_multiple_sentences:
                response = assistant.respond(utterance)
                utterance = ''


    start_conversation(False)