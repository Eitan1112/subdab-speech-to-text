# Syncit Speech to Text API
This is an API designed to convert speech to text.

## Routes
### /Convert - POST
Convert speech to text.
Form parameters:
language (str): for example 'en-US'.
hot_word (str): Word to look for.
frame_data_base64 (str): Base64 of the audio file frame data.
sample_rate (int): Sample rate.
sample_width (int): Sample width.

Client Usage:
```python
import requests
import speech_recognition as sr
import base64

URL = f'https://192.168.182.134:5000/Convert'
HOT_WORD = 'to'
LANGUAGE = 'en-US'

def main():
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile('audio.wav')

    with audio_file as source:
        audio = recognizer.record(audio_file, offset=50 ,duration=8)

    data = {
        'frame_data_base64': base64.b64encode(audio.frame_data),
        'sample_rate': audio.sample_rate,
        'sample_width': audio.sample_width,
        'language': LANGUAGE,
        'hot_word': HOT_WORD
    }

    response = requests.post(URL, data=data)
    transcript = response.text

if(__name__ == '__main__'):
    main()
```