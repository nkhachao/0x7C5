from reference_models.dialogpt import DialoGPT as Chatbot
from googletrans import Translator
import streamlit as st
import streamlit_chat as stc


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    st.session_state['chatbot'] = Chatbot()

    st.session_state['translator'] = Translator()
    st.session_state['input language'] = 'vi'
    st.session_state['show translation'] = False


def reset_conversation():
    st.session_state['chatbot'].reset()
    st.session_state['message_history'] = []


st.title('Multi-turn chatbot (Development prototype)')


with st.sidebar:
    st.title("Settings")
    if st.button('Reset conversation'):
        reset_conversation()

    language = st.radio("Language (powered by Google Translate)", ('English', 'Vietnamese'))
    st.session_state['input language'] = 'vi' if language == 'Vietnamese' else 'en'

    st.session_state['show translation'] = st.checkbox('Show english translations')


user_message = st.text_input("You:")

if user_message:
    input_language = st.session_state['input language']

    if input_language != 'en':
        translated_user_message = st.session_state['translator'].translate(user_message, src=input_language, dest='en').text
        response = st.session_state['chatbot'].reply(translated_user_message)
        translated_response = st.session_state['translator'].translate(response, src='en', dest=input_language).text

        show_translation = st.session_state['show translation']
        displayed_user_message = user_message + ' (' + translated_user_message + ')' if show_translation else user_message
        displayed_bot_response = translated_response + ' (' + response + ')' if show_translation else translated_response
        st.session_state['message_history'].append((displayed_user_message, True))
        st.session_state['message_history'].append((displayed_bot_response, False))

    else:
        response = st.session_state['chatbot'].reply(user_message)
        translated_response = st.session_state['translator'].translate(response, src='en', dest=input_language).text

        st.session_state['message_history'].append((user_message, True))
        st.session_state['message_history'].append((response, False))


for message, is_user in st.session_state['message_history']:
    stc.message(message, is_user=is_user)