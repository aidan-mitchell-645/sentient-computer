import speech_recognition as sr
import openai
from gtts import gTTS
import pygame
import sys
import time
from PIL import Image
import requests

# Set up API key for OpenAI
openai.api_key = "<token here>"

def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = r.listen(source)
    try:
        wake_word = r.recognize_google(audio)
        if wake_word.lower() == "computer":
            wake_word_detected()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))


def wake_word_detected():
    tts = gTTS("yes")
    tts.save("yes.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("yes.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    print("yes")
    listen_for_prompt()

def listen_for_prompt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for prompt...")
        audio = r.listen(source)
    try:
        prompt = r.recognize_google(audio)
        if prompt.lower() == "end simulation":
            sys.exit()
        else:
            send_prompt_to_openai(prompt)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

def send_prompt_to_openai(prompt):
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=2048,
                n=1,
                stop=None,
                temperature=0.5
            )
            output_response(response)
            break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(60)
            else:
                raise e

def output_response(response):
    response_text = response["choices"][0]["text"]
    tts = gTTS(response_text)
    tts.save("response.mp3")
    print("Response: " + response_text)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    gif = Image.open("face.gif")
    gif.seek(0)
    n_frames = gif.n_frames
    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        try:
            frame = gif.copy()
            frame.save("frame.png")
            face = pygame.image.load("frame.png")
            screen.blit(face, (0, 0))
            pygame.display.flip()
            gif.seek(gif.tell() + 1)
            if gif.tell() == n_frames - 1:
                gif.seek(0)
            pygame.time.Clock().tick(5)
        except EOFError:
            pass
    pygame.quit()

while True:
    listen_for_wake_word()