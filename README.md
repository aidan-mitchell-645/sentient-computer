# sentient-computer
A small python script which uses the openai api to talk back to you. I used openai to entirely script this.


Forgive my documentation. Heres how I got all of the packages for MacOS: 

```
brew install flac 
brew install portaudio  
pip3 install pyaudio  
pip3 install gTTS
pip3 install openai  
pip3 install SpeechRecognition  
pip3 install playsound 
pip3 install pygame
pip3 install spotipy 
Pip3 install Pillow
```

To run the bot: 

```
python3 chatgptbot.py
```

It responds to the wake word computer with a yes. Then listens to your prompt, sends it out to openai. Then outputs the resonse while playing the gif so it looks like the robot is talking. 
