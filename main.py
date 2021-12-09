from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
from os.path import exists

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)
speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0")

todo_list = ['Work on Veda', 'Clean up code', 'Develop new app']

VERSION = "Veda_v0.01"


# TODO: add new features (Skills) for Veda to perform
def create_note():
    
    global recognizer

    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.5)

                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

def add_todo():

    global recognizer

    speaker.say("What todo do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again!")
            speaker.runAndWait()


def show_todos():

    speaker.say("The items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    
    speaker.say("Hello. What can I do for you?")
    speaker.runAndWait()

def my_name():

    speaker.say("My name is Veda")
    speaker.runAndWait()

def quit():

    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    "greetings": hello,
    "my_name": my_name,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)

# TODO: Need to delete or replace old versions, also place new versions in folder
if exists(VERSION + '.h5'):
    assistant.load_model(model_name=VERSION)

else:
    assistant.train_model()
    assistant.save_model(model_name=VERSION)

# TODO: Need to add a wake up word for Veda to repond too
while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()