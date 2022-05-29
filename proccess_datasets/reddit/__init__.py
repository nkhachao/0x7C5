from efficientconvokit import Corpus, download
from tqdm import tqdm
import json
import time


def process_corpus(corpus, processed_data):
    for conversation_root in tqdm(corpus.get_conversation_roots()):
        conversations = corpus.get_longest_conversation(conversation_root)

        for conversation in conversations:
            messages = []
            previous_speaker = None

            for i, utterance in enumerate(conversation):
                text = utterance.text
                speaker = utterance.speaker

                # Preprocessing
                text = text.replace('\n\n', ' ').replace('\n', ' ')

                if i > 0 and speaker == previous_speaker:  # one speaker, multiple comments
                    messages[-1] += '. ' + text
                else:
                    messages.append(text)

                previous_speaker = speaker

            if len(messages) > 1:
                processed_data.append(messages)


subreddits = ['subreddit-ApplyingToCollege', 'subreddit-Cornell', 'subreddit-stanford', 'subreddit-yale', 'subreddit-princeton', 'subreddit-queensuniversity', 'subreddit-rmit', 'subreddit-nyu', 'subreddit-college', 'subreddit-education', 'subreddit-school', 'subreddit-highschool', 'subreddit-learnprogramming', 'subreddit-UBreddit', 'subreddit-uwaterloo', 'subreddit-UIUC', 'subreddit-berkeley', 'subreddit-UTAustin', 'subreddit-TaylorSwift', 'subreddit-CasualConversation', 'subreddit-MachineLearning', 'subreddit-socialskills', 'subreddit-cscareerquestions', 'subreddit-datascience', 'subreddit-MakeNewFriendsHere', 'subreddit-AskComputerScience',  'subreddit-Needafriend', 'subreddit-friendship', 'subreddit-askscience', 'subreddit-oxforduni', 'subreddit-URochester', 'subreddit-UofT', 'subreddit-nus', 'subreddit-explainlikeimfive', 'subreddit-travel', 'subreddit-BuyItForLife']
processed_data = []

for subreddit in subreddits:
    corpus = Corpus(filename=download(subreddit))

    corpus.print_summary_stats()
    process_corpus(corpus, processed_data)
    print('TOTAL CONVERSATIONS:', len(processed_data))

    with open('reddit.json', 'w') as fp:
        json.dump(processed_data, fp)


for i in range(5):
    for text in processed_data[i]:
        print(text)
        print('--------')

    print('====================')