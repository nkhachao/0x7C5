from Tagger import pos_tag, ner_tag, reminders_tag
from LongTermMemory import long_term_memory
from IntentClassifier import classify
from DataTypes import DataTypes, Task
from datetime import datetime


class MemorizationApp():
    def create_task(self, message):
        name = self.extract_name(message)
        if name:
            return Task('memorization', {'id': None, 'Details': {'Name': name}})

    def process_task(self, task, message):
        pos_text, pos_tags = pos_tag(message)

        contact_data = self.extract_contact_data(pos_text, pos_tags)
        for key, value in contact_data.items():
            if not task.data['Details'].get(key, None):
                task.data['Details'][key] = value

        if task.data.get('Resolve', None):
            if task.data['Resolve'] == 'CONFIRM NEW CONTACT':
                task.data['Resolve'] = None
                if classify(message, ['confirm', 'deny']) == 'deny':
                    task.response = 'Oh. Somehow don\'t know who this is. Do you want me to remember them?'
                    task.data['Resolve'] = 'CONFIRM ADD'
                    return

            if task.data['Resolve'] == 'CONFIRM ADD':
                task.data['Resolve'] = None
                if classify(message, ['confirm', 'deny']) == 'deny':
                    task.response = 'Ok. I won\'t remember them'
                    task.cancel()
                    return

        else:
            target_entities = long_term_memory.find_name(task.data['Details']['Name'])
            if target_entities.empty:
                task.response = 'You\'ve never mentioned ' + task.data['Details']['Name'] + ' before. Is this someone new?'
                task.data['Resolve'] = 'CONFIRM NEW CONTACT'
                return

            elif len(target_entities) == 1 and task.data['Details'].get('Role', None) is None:
                task.data['id'] = target_entities.index[0]
            else:
                mask = []
                if task.data['Details'].get('Role', None):
                    for role in target_entities['Role']:
                        if role:
                            if role.lower() == task.data['Details']['Role'].lower():
                                mask.append(True)
                            else:
                                mask.append(False)
                        else:
                            mask.append(False)

                filtered_targets = target_entities[mask]
                if len(filtered_targets) == 1:
                    task.data['id'] = filtered_targets.index[0]
                elif len(filtered_targets) > 1:
                    task.data['Resolve'] = target_entities
                    response = 'Which ' + task.data['Details']['Name'] + ' do you mean? '
                    for role in target_entities['Role']:
                        if role:
                            response += 'your ' + role + ', '
                    task.response = response + 'or a new person?'
                    return

        if task.data.get('id', None) is not None:
            long_term_memory.modify_contact(task.data['id'], task.data['Details'])
            task.response = 'I now know more about ' + task.data['Details']['Name'] + '\'s ' + ', '.join([x.lower() for x in task.data['Details']])
        else:
            long_term_memory.add_contact(task.data['Details'])
            task.response = 'Ok. Now I know about ' + task.data['Details']['Name']
            if task.data['Details'].get('Role', None):
                task.response += ', your ' + task.data['Details']['Role'].lower()
            else:
                task.response += '.'

        task.complete()

    def extract_name(self, message):
        pos_text, pos_tags = pos_tag(message)

        for text, tag in zip(pos_text, pos_tags):
            if tag == 'NNP':
                return text

    def extract_contact_data(self, pos_text, pos_tags):
        contact_data = {}
        nouns = []
        noun = ''
        for i, text, tag in zip(range(len(pos_text)), pos_text, pos_tags):
            if text == '@':
                contact_data['Email'] = pos_text[i - 1] + text + pos_text[i + 1]

            if tag == 'CD' and (len(text) == 10 or len(text) == 11):
                contact_data['Phone number'] = ('+' if text[0:2] == '84' else '') + text

            if tag == 'NN':
                if not noun:
                    noun = text
                elif pos_tags[i - 1] == 'NN':
                    noun += ' ' + text
                else:
                    nouns.append(noun)
                    noun = text

        if noun:
            nouns.append(noun)

        for noun in nouns:
            if classify(noun, ['a relationship', 'a role', 'other']) != 'other':
                contact_data['Role'] = noun
                break

        return contact_data


class Reminder:
    title = None
    date = None