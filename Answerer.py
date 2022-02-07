from transformers import TapasTokenizer, TapasForQuestionAnswering
from transformers import pipeline

model_name = 'google/tapas-base-finetuned-wtq'
model = TapasForQuestionAnswering.from_pretrained(model_name)
tokenizer = TapasTokenizer.from_pretrained(model_name)


def query_table(table, queries):
    inputs = tokenizer(table=table, queries=queries, padding='max_length', return_tensors="pt")
    outputs = model(**inputs)
    predicted_answer_coordinates, predicted_aggregation_ids = tokenizer.convert_logits_to_predictions(
             inputs,
             outputs.logits.detach(),
             outputs.logits_aggregation.detach()
     )

    answers = []
    for coordinates in predicted_answer_coordinates:
        cell_values = []
        for coordinate in coordinates:
            cell_values.append(table.iat[coordinate])
        answers.append(cell_values)

    final_answers = []

    try:
        for answer, predicted_aggregation_id in zip(answers, predicted_aggregation_ids):
            if predicted_aggregation_id == 0:  # NONE
                final_answers.append(answer)
                continue
            elif predicted_aggregation_id == 1:     # SUM
                values = [float(x) for x in answer]
                final_answers.append([str(sum(values))])
            elif predicted_aggregation_id == 2:     # AVERAGE
                values = [float(x) for x in answer]
                if len(values) == 0:
                    final_answers.append(['0'])
                else:
                    final_answers.append([str(sum(values)/len(values))])
            elif predicted_aggregation_id == 3:     # COUNT
                final_answers.append([str(len(answer))])
    except ValueError:
        for answer, predicted_aggregation_id in zip(answers, predicted_aggregation_ids):
            final_answers.append(answer)

    return final_answers


def single_query_table(table, query):
    return query_table(table, [query])[0]


qa_pipeline = pipeline(
    "question-answering",
    model="csarron/bert-base-uncased-squad-v1",
    tokenizer="csarron/bert-base-uncased-squad-v1"
)

def query_passage(passage, query):
    predictions = qa_pipeline({'context': passage, 'question': query})
    return predictions['answer']


