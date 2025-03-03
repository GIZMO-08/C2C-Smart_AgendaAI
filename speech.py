## focusing on putting speech recognition into the ai

# windows install on pip: py -m venv <your-env>
#.\<your-env>\Scripts\activate
#pip install google-cloud-speech


#mac
#python3 -m venv <your-env>
#source <your-env>/bin/activate
#pip install google-cloud-speech

#documentation link:https://pypi.org/project/google-cloud-speech/


import sounddevice as sd
import wavio as wv #pip install wavio


#sample frequency

freq = 44100

#recording max length

duration = 30
#start the recorder

recording = sd.rec(int(duration * freq),sampleRate = freq,
channels = 2)

sd.wait()


#create audio file
wv.write("recording1.wav", freq, recording)

#obtained from:
#https://www.geeksforgeeks.org/create-a-voice-recorder-using-python/

from google.cloud import speech_V1 as speech

def function1(config,audio):
    client = speech.speechClient()
    response = client.recognize(config,audio)

config = {"language_code":"en-US"}
audio = {'uri': 'gs://cloud-samples-data/speech/brooklyn_bridge.flac'}



from openai import OpenAI
client = OpenAI()

audio_file= open("/path/to/file/audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
)

print(transcription.text)


