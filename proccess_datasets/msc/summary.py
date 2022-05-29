import pyjsonviewer
import json

directory = '/Users/haonguyen/Documents/Python Environments/Python 3.9/lib/python3.9/site-packages/data/msc/msc/msc_personasummary/'
sessions = ['session_1/', 'session_2/', 'session_3/', 'session_4/']


def get_summary_data(split):
    data = {}

    for session in sessions:
        if 'session_4' in session and 'train' in split:     # train split doesnt include session 4
            break

        with open(directory + session + split + '.txt', 'r') as f:
            conversations = f.readlines()

        for conversation_text in conversations:
            conversation_data = json.loads(conversation_text)
            new_fact = conversation_data['newfact']
            conversation_id = conversation_data['initial_data_id']

            if conversation_id in data:
                data[conversation_id]['new facts'].append(new_fact)
            else:
                data[conversation_id] = {'new facts':[new_fact]}

    print('summary -', split + ':', len(data), 'conversations')


    return data


if __name__ == "__main__":
    with open(directory + sessions[1] + 'train.txt','r') as f:
        lines = f.readlines()

    pyjsonviewer.view_data(json_data=json.loads(lines[3]))