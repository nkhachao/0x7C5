from References.DialoGPT import DialoGPT
import pyttsx3
from flask import Flask, render_template, request
import threading

chatbot = DialoGPT()
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

    while True:
        try:
            response = chatbot.reply(utterance)
            t1 = threading.Thread(target=speak, args=(response,))
            t1.start()
            t1.join()
            return response
        except:
            return 'I crashed and restarted!'



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
