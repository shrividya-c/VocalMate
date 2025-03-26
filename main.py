from datetime import datetime
import threading
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
from groq import Groq
import wikipedia
import random
import time
import musicLibrary

recognizer = sr.Recognizer()
engine = pyttsx3.init()

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

exit_keywords = ["exit", "quit", "goodbye", "bye", "stop", "shut down", "close"]

# function to speak the text using pyttsx3
def speakOld(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.say(text)
    engine.runAndWait()

# Function to wish the user based on the time of the day
def wishMe():
    hour = int(datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Virtual Assistant, Zara. Please tell me how may I help you")

# function to speak the text using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')

    try:
        tts.save("speech.mp3")
    except PermissionError:
        time.sleep(1)  # Wait for the file to be available
        tts.save("speech.mp3")

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load a sound file (use a valid path to an audio file, like .wav, .mp3, etc.)
    pygame.mixer.music.load('speech.mp3')

    # Play the music
    pygame.mixer.music.play()

    # To check if music is still playing, if yes, wair for it to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Wait before deleting to ensure it's not in use
    time.sleep(1)
    try:
        os.remove("speech.mp3")
    except PermissionError:
        print("Warning: Unable to delete the file. Will try again later.")

# function to handle the AI processing
def aiProcessCommand(command):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Zara skilled in general tasks like opening websites, playing music, and fetching the news. Give short responses."
            },
            {
                "role": "user",
                "content": command
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# function to perform the tasks based on the command
def processCommand(command):
    # Open websites
    if "open google" in command.lower():
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command.lower():
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command.lower():
        speak("Opening Facebook...")
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in command.lower():
        speak("Opening LinkedIn...")
        webbrowser.open("https://www.linkedin.com")
    elif "wikipedia" in command.lower():
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak(f"According to Wikipedia, {results}")      
        print(f"According to Wikipedia:\n{results}")

    # Play music from youtube
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        speak(f'Playing {song}...')
        link = musicLibrary.music[song]
        webbrowser.open(link)

    # Play music from my system
    elif "songs from my system" in command.lower():
        speak("Playing songs from your system...")
        music_dir = "D:\\Music"
        songs = [file for file in os.listdir(music_dir)]
        random_song = random.choice(songs)
        speak(f"Playing {random_song}")
        print('Playing:', random_song)
        os.startfile(os.path.join(music_dir, random_song))
        
    # Tell the current time
    elif "time" in command.lower():
        strTime = datetime.now().strftime("%H:%M:%S")    
        speak(f"The time is {strTime}")
        print(f"The time is {strTime}")

    # Fetch the news
    elif "news" in command.lower():
        speak("Getting the news...")
        print("Today's headlines are:")
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}')
        if r.status_code == 200:
            data = r.json()
            # Extracting the titles from the articles
            titles = [article['title'] for article in data['articles']]
            short_titles = titles[:5]  # Get the first 5 titles
            rest_titles = titles[5:]  # Get the rest of the titles
            # Print the extracted titles
            for title in short_titles:
                speak(title)
                print(title)
            # Ask the user if they want to hear more news
            speak("Would you like to hear more news?")
            more_news = input("Would you like to hear more news? (yes/no): ")
            if more_news.lower() == "yes":
                for title in rest_titles:
                    speak(title)
                    print(title)
    
    # Terminate the virtual assistant
    elif any(key in command.lower() for key in exit_keywords):
        speak("Goodbye!")
        print("Goodbye!")
        exit()

    else:
        # let the Grok AI process the command
        output = aiProcessCommand(command)
        speak(output)
        print(output)


def remind_to_drink_water():
    # Function to remind the user to drink water every hour.
    while True:
        time.sleep(1*60*60)  # Wait for 1 hour
        speak("Time to drink some water. Stay hydrated!")

# Start the water reminder in a separate thread
reminder_thread = threading.Thread(target=remind_to_drink_water, daemon=True)       
reminder_thread.start()          



if __name__ == "__main__":
    # wish the user
    wishMe()
    # speak("Initialising Zara...")   
    while True:
        # obtain audio from the microphone"
        r = sr.Recognizer()      
        # print("Recognizing...")      
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            # recognize speech using Google Speech Recognition
            word = r.recognize_google(audio)
            # listen to the wake word "Zara"
            if word.lower() == "zara":
                speak("Yes, I'm listening")
                # listen to the command
                with sr.Microphone() as source:
                    print("Zara active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"User said: {command}")
                    processCommand(command)
                    
        except Exception as e:
            print("Please repeat...")