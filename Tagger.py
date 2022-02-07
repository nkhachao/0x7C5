from flair.data import Sentence
from flair.models import SequenceTagger
from tensorflow import keras
from BERT import tokenize, tokenizer, embed
import numpy as np

# load tagger
NER_tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")
POS_tagger = SequenceTagger.load("flair/pos-english")
reminders_tagger = keras.models.load_model('models/reminders_title_extractor_1989')


def ner_tag(sentence):
    flair_sentence = Sentence(sentence)

    NER_tagger.predict(flair_sentence)

    result = []
    for entity in flair_sentence.get_spans('ner'):
        result.append((entity.text, entity.tag))

    return result


def pos_tag(sentence):
    flair_sentence = Sentence(sentence)

    POS_tagger.predict(flair_sentence)

    text = []
    tags = []
    for entity in flair_sentence.get_spans('pos'):
        text.append(entity.text)
        tags.append(entity.tag)

    return text, tags


def reminders_tag(sentence):
    embeddings = embed(sentence)
    predictions = np.squeeze(reminders_tagger(embeddings['full']).numpy())
    tokens = np.squeeze(tokenize(sentence)['input_ids'].numpy())

    mask = predictions != 0
    filtered = tokens[mask]

    return tokenizer.decode(filtered)

