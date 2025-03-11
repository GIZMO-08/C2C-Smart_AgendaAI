## focusing on putting speech recognition into the ai

# windows install on pip: py -m venv <your-env>
#.\<your-env>\Scripts\activate
#pip install google-cloud-speech


#mac
#python3 -m venv <your-env>
#source <your-env>/bin/activate
#pip install google-cloud-speech

#documentation link:https://pypi.org/project/google-cloud-speech/
import whisper
import pyaudio
import wave 
import keyboard
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "recording1.wav"
RECORD_SECONDS = 60

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []

print("debug log: press Space to start recording")
keyboard.wait('space')
print("Debug log: recording... [Space] or wait 60 seconds for stop")
time.sleep(0.2)

while true:
  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:
      data = stream.read(CHUNK)
      frames.append(data)
    except KeyboardInterrupt:
        break
      if keyboard.is_pressed('space')
        print("Recording stopping...")
        time.sleep(0.2)
        break

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

#whisper import and setup


model = whipser.load_model("large-v2")
result = model.transcribe("recording1.wav")
print(result["text"])

from transformers import pipeline 
transcriber = pipeline(model= "openai/whisper-large-v2",device=0,batch_size=2)


from openai import OpenAI
client = OpenAI()

client.files.create(
  file=open("mydata.jsonl", "rb"),
  purpose="fine-tune"
)


audio_filenames = ["recording1.wav"]
texts = transcriber(audio_filenames)
print(texts)


writer = get_writer(texts, output_dir)
writer(result, audio_path)


#from openai import OpenAI
#client = OpenAI()

#audio_file= open("/path/to/file/audio.mp3", "rb")
#transcription = client.audio.transcriptions.create(
#    model="whisper-1", 
 #   file=audio_file
#)

#print(transcription.text)


