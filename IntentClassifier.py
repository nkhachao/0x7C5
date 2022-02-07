import numpy as np
from tensorflow import keras
from BERT import embed
from transformers import pipeline


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
op_intent_classifier = keras.models.load_model('models/op_intent_classifier')


def classify(text, labels):
    results = classifier(text, labels)
    return results['labels'][np.argmax(results['scores'])]


def classify_intent(text):
    result = []
    a = classify(text, ['ask for information', 'request to remind later', 'provide information', 'request to send emails', 'other'])
    if a == 'request to remind later':
        result.append('reminders')
        b = classify(text, ['yes/no question', 'other'])
        if b == 'yes/no question':
            result.append('requires task confirmation')

    elif a == 'ask for information':
        result.append('information retrieve')
        b = classify(text, ['ask about tasks', 'other'])
        if b == 'ask about tasks':
            result.append('reminders')

    elif a == 'other' or a == 'provide information':
        result = ['inform']
        b = classify(text, ['tasks', 'relationships', 'other'])

    print('*', result)
    return result


def classify_op_intent(text):
    intents = ['OTHER', 'ADD', 'EDIT', 'REMOVE', 'UNDO_OR_REDO']
    embeddings = embed(text)
    intent = op_intent_classifier(embeddings['pooled'])
    print('op:', intents[intent[0]])
    return intents[intent[0]]