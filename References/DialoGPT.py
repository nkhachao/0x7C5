from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class DialoGPT:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
        self.chat_history_ids = torch.LongTensor([[]])
        self.previous_response = ''

    def reply(self, message):
        # Add the new user input tokens to the chat history
        new_message_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt')
        self.chat_history_ids = torch.cat([self.chat_history_ids, new_message_ids], dim=-1)

        # Transformer-based language generation models tend to repeat the same thing. This is a known issue.
        # https://github.com/microsoft/DialoGPT/issues/45
        # https://arxiv.org/pdf/1911.00536.pdf - 5.2 Addressing Cross-turn Repetitions
        # Generate a new response until we get one that doesn't repeat the last response
        # Generate a new response until we get one that doesn't repeat the user's message

        response, chat_history_ids = self.generate_candidate_response()

        while response.lower() == self.previous_response.lower() or response.lower() == message.lower():
            response, chat_history_ids = self.generate_candidate_response()

        self.previous_response = response
        self.chat_history_ids = chat_history_ids

        return response

    def generate_candidate_response(self):
        # Model adds its response tokens to chat history ids. Conversation length is limited to 1000 tokens

        # Beam search tries to choose the most probable answer possible
        # But human likes to be surprised by the responses, so some randomness is needed
        # Using beam search with 2 beams and sampling

        outputs = self.model.generate(self.chat_history_ids, max_length=1000,
                                      pad_token_id=self.tokenizer.eos_token_id,
                                      num_beams=2, do_sample=True,
                                      return_dict_in_generate=True, output_scores=True)

        chat_history_ids = outputs['sequences']
        chat_history = self.tokenizer.decode(chat_history_ids[0])

        return chat_history.split('<|endoftext|>')[-2], chat_history_ids

    def reset(self):  # Reinitialize this class is really slow. So we need a reset method instead
        self.chat_history_ids = torch.LongTensor([[]])
