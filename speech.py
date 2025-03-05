## focusing on putting speech recognition into the ai

# windows install on pip: py -m venv <your-env>
#.\<your-env>\Scripts\activate
#pip install google-cloud-speech


#mac
#python3 -m venv <your-env>
#source <your-env>/bin/activate
#pip install google-cloud-speech

#documentation link:https://pypi.org/project/google-cloud-speech/

#recording feature
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


#whisper import and setup
import whisper

model = whipser.load_model("large-v2")
result = model.transcribe("recording1.wav")
print(result["text"])

from transformers import pipeline 
transcriber = pipeline(model= "openai/whisper-large-v2",device=0,batch_size=2)

audio_filenames = ["recording1.wav"]
texts = transcriber(audio_filenames)
print(texts)


#from openai import OpenAI
#client = OpenAI()

#audio_file= open("/path/to/file/audio.mp3", "rb")
#transcription = client.audio.transcriptions.create(
#    model="whisper-1", 
 #   file=audio_file
#)

#print(transcription.text)


