from Assistant import Assistant
from LongTermMemory import LongTermMemory
from ShortTermMemory import ShortTermMemory
import pyttsx3
from flask import Flask, render_template, request
import threading

assistant = Assistant()
app = Flask(__name__)
engine = pyttsx3.init(driverName='nsss')

def speak(text):
    if engine._inLoop:
        engine.endLoop()
    engine.say(text)
    engine.runAndWait()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    utterance = request.args.get('msg')

    if utterance == 'RESET':
        global short_term_memory
        global long_term_memory

        short_term_memory = ShortTermMemory()
        long_term_memory = LongTermMemory()
        return ''

    while True:
        try:
            response = assistant.respond(utterance)
            t1 = threading.Thread(target=speak, args=(response,))
            t1.start()
            t1.join()
            return response
        except:
            return 'I crashed and restarted!'

    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
