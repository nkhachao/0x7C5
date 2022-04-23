from References.DialoGPT import DialoGPT as Chatbot
import gradio as gr

chatbot = Chatbot()


def chat(message, history):
    history = history or []       # Or returns the first True item or the last item

    if not history:
        chatbot.reset()

    response = chatbot.reply(message)
    history.append((message, response))

    return history, history


iface = gr.Interface(
    chat,
    ["text", "state"],
    ["chatbot", "state"],
    allow_screenshot=False,
    allow_flagging="never",
)

iface.launch()