from gtts import gTTS
import os
import playsound


def speak(text):
    tts = gTTS(text=text, lang='en')

    filename = "abc.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


speak("Is this someone new?")


#exit()

import pyttsx3
engine = pyttsx3.init(driverName='nsss')
engine.runAndWait()
engine.say("I don't know anything about this, sorry. You've never mentioned John before. Is this someone new?")
engine.runAndWait()
engine.endLoop()   # add this line
engine.stop()
print("I don't know anything about John. Is this someone new? Can you tell me more about him?")