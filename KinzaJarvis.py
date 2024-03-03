import os
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import openai
import time
import playsound

api_key = "sk-gby29nzkUAaWMBQ4kFJVA3jv3N5t7qCGR5TZK9a" # I changed some character for my API key, it will not work for you, please use your own chat GPT and obtain an API key. 
lang = 'en'
openai.api_key = api_key

def speak(text):
    speech = gTTS(text=text, lang=lang, slow=False)
    speech.save("output.mp3")
    playsound.playsound("output.mp3")

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source: #if you dont have a microphone, you can change how the audio is obtained. :) 
        print("I am listening...")
        audio = r.listen(source)
    return r.recognize_google(audio)

exit_phrases = ["Exit", "Please Stop", "Stop", "End Now"]

try:
    speak("Go ahead and say something... ")
    audio_text = get_audio()
    print("You said: ", audio_text)

    for phrase in exit_phrases:
        if phrase.lower() in audio_text.lower():
            print("Stopping now...")
            break

    if "Jarvis" in audio_text:
        words = audio_text.split()
        new_string = ' '.join(words[1:])
        print(new_string)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "user", "content": audio_text}])
        text = completion.choices[0].message.content
        speak(text)

except sr.UnknownValueError:
    print("Could not understand audio....")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
except Exception as e:
    print("Exception:", e)

