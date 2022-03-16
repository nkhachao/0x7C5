from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class DialoGPT:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
        self.chat_history_ids = torch.LongTensor([[]])

    def reply(self, message):
        # Add the new user input tokens to the chat history
        new_message_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt')
        self.chat_history_ids = torch.cat([self.chat_history_ids, new_message_ids], dim=-1)

        # Model adds its response tokens to chat history ids. Input is limited to 1000 tokens
        # Transformer-based language generation models tend to repeat the same thing. This is a known issue.
        # https://github.com/microsoft/DialoGPT/issues/45
        self.chat_history_ids = self.model.generate(self.chat_history_ids, max_length=1000,
                                                    pad_token_id=self.tokenizer.eos_token_id, do_sample=True,
                                                    top_k=0,
                                                    top_p=0.45)

        chat_history = self.tokenizer.decode(self.chat_history_ids[0])
        return chat_history.split('<|endoftext|>')[-2]

    def reset(self):    # Reinitialize this class is really slow. So we need a reset method instead
        self.chat_history_ids = torch.LongTensor([[]])