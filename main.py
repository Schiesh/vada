import os
import time
import queue
from datetime import date
from pygame import mixer
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    mixer.init()
    tempText = text.replace(" ", "_")
    filename = "audio/" + tempText + ".mp3"
    if os.path.exists(filename):
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
        mixer.quit()

    else:
        tts = gTTS(text=text, lang="en")    
        tts.save(filename)
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(1)
        mixer.quit()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said.lower())
        except Exception as e:
            print("Did not recognize input "+ str(e))

    return said.lower()

WAKE = "okay"
q = queue.Queue()
print("Start")

while True:
    print("Listening")

    while q.empty():
        mess = get_audio()
        q.put(mess)

    message = q.get()  

    if message.count(WAKE) > 0:
        speak("How may I assist you")
        message = get_audio()

        if "hello" in message:
            speak("Hello how are you")

        if "your name" in message:
            speak("My name is Veda")

        if "today's date" in message:
            today = date.today()
            date = today.strftime("%B %d %Y")
            speak("Today is " + date)
            dateTemp = date.replace(" ", "_")
            os.remove("audio/Today_is_" + dateTemp + ".mp3")
        
        if "bye" in message:
            speak("Have a nice day")
            speak("Good bye")