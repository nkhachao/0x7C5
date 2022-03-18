from References.DialoGPT import DialoGPT as Chatbot
import pyttsx3
from datetime import datetime
from flask import Flask, render_template, request
import threading

chatbot = Chatbot()
app = Flask(__name__)
engine = pyttsx3.init(driverName='nsss')


def log(text):
    with open('Demo/Log.txt', 'a') as file:
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        file.write('\n(' + current_time + ') ' + text)


def speak(text):
    if engine._inLoop:
        engine.endLoop()
    engine.say(text)
    engine.runAndWait()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_response")
def get_bot_response():
    message = request.args.get('msg')

    try:
        response = chatbot.reply(message)
        t1 = threading.Thread(target=speak, args=(response,))
        t1.start()
        t1.join()
    except:
        response = 'I crashed and restarted!'

    log('Human: ' + message)
    log('Bot: ' + response)
    return response


@app.route("/reset_conversation", methods=['POST'])
def reset_conversation():
    global chatbot
    chatbot.reset()
    log('------ New conversation started ------')
    print('------ New conversation started ------')
    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
