from reference_models.dialogpt import DialoGPT
from hex7c5_msc import HEX7C5_MSC
from hex7c5_reddit import HEX7C5_REDDIT
from googletrans import Translator
import streamlit as st
import streamlit_chat as stc


class ChatbotApp:
    def __init__(self):
        self.show_translation = False
        self.language = 'English'
        self.model_name = 'DialoGPT'
        self.message_history = []
        self.chatbot = DialoGPT()
        self.translator = Translator()

    def display_reset_button(self):
        if st.button('Reset conversation'):
            self.reset_conversation()

    def display_language_options(self):
        language = st.radio("Language (powered by Google Translate)", ('English', 'Vietnamese'))
        if language != self.language:
            self.reset_conversation()
            self.language = language

    def display_translation_toggle(self):
        self.show_translation = st.checkbox('Show english translations')

    def display_model_options(self):
        model = st.radio("Model", ('DialoGPT', 'Prototype (MSC)', 'Prototype (Reddit)'))
        if model != self.model_name:
            self.reset_conversation()

            if model == 'DialoGPT':
                self.chatbot = DialoGPT()
            elif model == 'Prototype (MSC)':
                self.chatbot = HEX7C5_MSC()
            elif model == 'Prototype (Reddit)':
                self.chatbot = HEX7C5_REDDIT()

            self.model_name = model

    def reset_conversation(self):
        self.chatbot.reset()
        self.message_history = []


if 'app' not in st.session_state:
    st.session_state['app'] = ChatbotApp()

app = st.session_state['app']

st.title('Multi-turn chatbot (Development prototype)')

with st.sidebar:
    st.title("Settings")

    app.display_reset_button()
    app.display_language_options()
    app.display_translation_toggle()
    app.display_model_options()

user_message = st.text_input("You:")

if user_message:
    input_language = app.language

    if input_language != 'English':
        translated_user_message = app.translator.translate(user_message, src=input_language, dest='en').text
        response = app.chatbot.reply(translated_user_message)
        translated_response = app.translator.translate(response, src='en', dest=input_language).text

        show_translation = app.show_translation
        displayed_user_message = user_message + ' (' + translated_user_message + ')' if show_translation else user_message
        displayed_bot_response = translated_response + ' (' + response + ')' if show_translation else translated_response
        app.message_history.append((displayed_user_message, True))
        app.message_history.append((displayed_bot_response, False))

    else:
        response = app.chatbot.reply(user_message)
        translated_response = app.translator.translate(response, src='en', dest=input_language).text

        app.message_history.append((user_message, True))
        app.message_history.append((response, False))

for message, is_user in app.message_history:
    stc.message(message, is_user=is_user)
