from convokit import download
import json


class Corpus:
    def __init__(self, filename):
        self.filename = filename + '/utterances.jsonl'
        self.utterance_count = 0
        self.grouped_utterances = {}

        with open(self.filename) as infile:
            for line in infile:
                self.utterance_count += 1

                utterance_data = json.loads(line)

                conversation_root = utterance_data['root']
                root_text = utterance_data['text']

                if not self.is_bad(root_text):
                    if conversation_root in self.grouped_utterances:
                        self.grouped_utterances[conversation_root].append(Utterance(utterance_data))
                    else:
                        self.grouped_utterances[conversation_root] = [Utterance(utterance_data)]

    def print_summary_stats(self):
        print('Number of Utterances: ' + str(self.utterance_count))

    def get_conversation_roots(self):
        return self.grouped_utterances.keys()

    def get_conversations(self, conversation_root):     # There can be many replies to 1 comment, sparking many convos
        conversations = []
        utterances = self.grouped_utterances[conversation_root]

        for utterance in utterances:
            if utterance.id == conversation_root:
                conversations.append([utterance])
                break

        while True:     # Organize utterances into conversation threads
            changed = False
            updated_conversations = {}

            for utterance in utterances:
                for conversation_index, conversation in enumerate(conversations):
                    last_conversation_utterance = conversation[-1]

                    if utterance.reply_to == last_conversation_utterance.id:
                        changed = True
                        if conversation_index in updated_conversations:
                            updated_conversations[conversation_index].append(conversation + [utterance])
                        else:
                            updated_conversations[conversation_index] = [conversation + [utterance]]

            for conversation_index, conversation in enumerate(conversations):
                if conversation_index not in updated_conversations:
                    updated_conversations[conversation_index] = [conversation]

            if not changed:
                break
            else:
                conversations = []
                for updated_conversations in updated_conversations.values():
                    conversations += updated_conversations

        return self.filter_conversations(conversations)

    def get_longest_conversation(self, conversation_root):
        conversations = self.get_conversations(conversation_root)

        if conversations:
            return [max(conversations, key=len)]
        else:
            return conversations

    def filter_conversations(self, conversations):
        filtered_conversations = []
        for conversation in conversations:
            is_bad = False
            for utterance in conversation:
                text = utterance.text
                if self.is_bad(text):
                    is_bad = True
                    break

            if not is_bad:
                filtered_conversations.append(conversation)

        return filtered_conversations

    def is_bad(self, message):
        return '[deleted]' in message or '[removed]' in message or not message \
               or 'http' in message or len(message.split(' ')) > 128


class Utterance:
    def __init__(self, data):
        self.root = data['root']
        self.id = data['id']
        self.text = data['text']
        self.speaker = data['user']
        self.reply_to = data['reply_to']




