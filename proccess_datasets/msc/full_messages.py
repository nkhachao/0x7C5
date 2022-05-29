import pyjsonviewer
import json

directory = '/Users/haonguyen/Documents/Python Environments/Python 3.9/lib/python3.9/site-packages/data/msc/msc/msc_dialogue/'


def get_messages_data(split):
    data = {}

    sessions = ['session_4', 'session_3'] if 'train' in split else ['session_5', 'session_4', 'session_3']

    for session in sessions:    # scan from conversations with more sessions to conversations with fewer sessions
        with open(directory + session + '/' + split + '.txt', 'r') as f:
            conversations = f.readlines()

        for raw_conversation in conversations:
            conversation_data = json.loads(raw_conversation)

            conversation_id = conversation_data['metadata']['initial_data_id']
            if conversation_id in data:
                continue

            intervals = []
            messages = []

            for session_data in conversation_data['previous_dialogs']:      # Add previous sessions
                session_messages = [x['text'] for x in session_data['dialog']]
                interval = {'amount':session_data['time_num'], 'unit':session_data['time_unit']}

                messages.append({'messages':session_messages})
                intervals.append(interval)

            messages.append({'messages':[x['text'] for x in conversation_data['dialog']]})     # Add current session
            data[conversation_id] = {'sessions':messages, 'intervals':intervals}

        print('full messages -', split, ' + '.join(sessions[0:sessions.index(session) + 1]) + ':', len(data.keys()))

    return data


if __name__ == "__main__":
    get_messages_data('train')
    with open(directory + 'session_4/' + 'train.txt','r') as f:
        lines = f.readlines()

    pyjsonviewer.view_data(json_data=json.loads(lines[637]))