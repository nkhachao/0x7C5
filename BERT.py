from transformers import AlbertTokenizer, TFAlbertModel

tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
bert = TFAlbertModel.from_pretrained('albert-base-v2')

TOKEN_LIMIT = 384

cached_embeddings = {}


def tokenize(text):
    return tokenizer(text, padding='max_length', max_length=TOKEN_LIMIT, return_tensors="tf")


def embed(text):
    global cached_embeddings

    cached = cached_embeddings.get(text, None)
    if cached:
        return cached
    else:
        inputs = tokenize(text)
        outputs = bert(inputs)
        last_hidden_states = outputs.last_hidden_state
        pooled_output = outputs.pooler_output

        embeddings = {'full': last_hidden_states, 'pooled':pooled_output}
        if len(cached_embeddings) > 4:
            cached_embeddings = {}

        cached_embeddings[text] = embeddings
    return embeddings