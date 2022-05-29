from summary import get_summary_data
from full_messages import get_messages_data
import json
import pyjsonviewer

full_data = get_messages_data('train')
summary_data = get_summary_data('train')

for conversation_id, data in summary_data.items():
    if conversation_id in full_data:
        for i, summary in enumerate(data['new facts']):
            full_data[conversation_id]['sessions'][i]['summary'] = summary


with open('msc.json', 'w') as fp:
    json.dump(full_data, fp)

pyjsonviewer.view_data(json_data=full_data)