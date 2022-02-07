import pandas as pd
import random

reminders_template = ['Title', 'Time']
contacts_template = ['Name', 'Role', 'Phone number', 'Email']

class LongTermMemory():
    def __init__(self):
        self.reminders = pd.DataFrame(columns = reminders_template)

        self.contacts = pd.DataFrame(columns = contacts_template)

    def add_reminder(self, data):
        new_row = {}
        for column in reminders_template:
            new_row[column] = [data[column]]

        new_row = pd.DataFrame.from_dict(new_row)
        self.reminders = self.reminders.append(new_row, ignore_index=True)

    def add_contact(self, data):
        new_row = {}
        for column in contacts_template:
            if data.get(column, None):
                new_row[column] = [data[column]]
            else:
                new_row[column] = ['']

        new_row = pd.DataFrame.from_dict(new_row)
        self.contacts = self.contacts.append(new_row, ignore_index=True)
        print(self.contacts)

    def modify_contact(self, id, data):
        for column in contacts_template:
            if data.get(column, None):
                self.contacts.at[id, column] = data[column]

    def find_name(self, name):
        mask = []
        for value in self.contacts['Name']:
            if name.lower() == value.lower():
                mask.append(True)
            else:
                mask.append(False)

        print(self.contacts[mask])
        return self.contacts[mask]

    def find(self, data):
        result = self.contacts
        for field, value in data:
            result = result[result[field] == value]

        return result


long_term_memory = LongTermMemory()