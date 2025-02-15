## focusing on putting speech recognition into the ai

# windows install on pip: py -m venv <your-env>
#.\<your-env>\Scripts\activate
#pip install google-cloud-speech


#mac
#python3 -m venv <your-env>
#source <your-env>/bin/activate
#pip install google-cloud-speech


from google.cloud import speech_V1 as speech

def function1(config,audio):
    client = speech.speechClient()
    response = client.recognize(config,audio)

config = {"language_code":"en-US"}
audio = {'uri': 'gs://cloud-samples-data/speech/brooklyn_bridge.flac'}

