from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
chat_history_ids = torch.LongTensor([[]])

while True:
    new_message_ids = tokenizer.encode(input('User: ') + tokenizer.eos_token, return_tensors='pt')

    # Add the new user input tokens to the chat history
    chat_history_ids = torch.cat([chat_history_ids, new_message_ids], dim=-1)

    for _ in range(20):
        # Model adds its response tokens to chat history. Conversation length is limited to 1000 tokens
        # Using beam search mostly because huggingface only
        x = model.generate(chat_history_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id,
                           num_beams=2, do_sample=True,
                           return_dict_in_generate=True, output_scores=True)
        print(x['sequences_scores'][0])

        chat_history = tokenizer.decode(x['sequences'][0])
        print(chat_history)

    chat_history_ids = x

    print('DialoGPT: ', chat_history.split('<|endoftext|>')[-2])