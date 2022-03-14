from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class DialoGPT:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
        self.chat_history_ids = torch.LongTensor([[]])

    def reply(self, message):
        new_message_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt')

        # Add the new user input tokens to the chat history
        self.chat_history_ids = torch.cat([self.chat_history_ids, new_message_ids], dim=-1)

        # Model adds its response tokens to chat history. Input is limited to 100 tokens
        self.chat_history_ids = self.model.generate(self.chat_history_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)

        chat_history = self.tokenizer.decode(self.chat_history_ids[0])
        return chat_history.split('<|endoftext|>')[-2]