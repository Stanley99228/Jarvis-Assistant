import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit as kit
import aiml
import os
import warnings
warnings.filterwarnings("ignore")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
voices = engine.setProperty('voice', voices[0].id)



BRAIN_FILE = "brain.dump"

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading Brain" +BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)

else:
    k.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    print("Saving File" +BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss!")
    elif hour >= 12 and hour < 18:
        speak("Good Evening Boss!")
    else:
        speak("Good Afternoon Boss!")
    speak("Jarvis at you service sir.")


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("the current time is")
    speak(Time)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")

    except Exception as e:

        return "None"

    return query


def whatIs():
    speak("Showing results from Google")
    webbrowser.open("https://www.google.com/search?q=" + query)
    return


def whoIs():
    speak("Searching wikipedia")
    result = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    speak(result)
    speak("do you want a google search")
    condition = takeCommand().lower()
    if (condition == 'yes'):
        speak("Showing results from Google")
        webbrowser.open("https://www.google.com/search?q=" + query)
    elif (condition == 'none'):
        speak("showing results from google")
        webbrowser.open("https://www.google.com/search?q=" + query)

    elif (condition == "no"):
        return


def songs():
    speak("what song should i play?")
    y = takeCommand().lower()
    if (y == 'none'):
        pass
    else:
        print(y)
        speak("Playing" + y)
        kit.playonyt(y)


if __name__ == "__main__":
    wishme()
    while 1:
        query = takeCommand().lower()
        response = k.respond(query)           
        print(response)
        speak(response)


        if "who is" in query:
            query = query.replace("who is", " ")
            whoIs()
        elif 'bye' in query:
            speak('GoodBye Sir')
            quit()
        elif 'time' in query:
            time()

        elif 'what is ' in query:
            query = query.replace("what is", " ")
            whatIs()
            
        elif 'songs' or 'play' or 'song' in query:
            if 'songs' and 'song' in query:
                songs()
            elif 'play' in query:
                query = query.replace('play',' ')
                speak("playing"+query)
                kit.playonyt(query)

