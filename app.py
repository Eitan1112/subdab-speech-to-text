from flask import Flask, request, Response
import speech_recognition as sr
import json
import base64
import logging

ACCURACY = 1 # 0 to 1

logging.basicConfig(
     filename='debug.log',
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
	logger.debug(f"JSON: {request.form['hot_words']}")
	language = request.form['language'] 
	hot_words = [(hot_word, ACCURACY) for hot_word in json.loads(request.form['hot_words'])]
	recognizer = sr.Recognizer()
	frame_data_base64 = request.form['frame_data_base64']
	frame_data = base64.b64decode(frame_data_base64)
	sample_rate = int(request.form['sample_rate'])
	sample_width = int(request.form['sample_width'])

	logger.debug(f'Recieved request. Language: {language}. Hot word: {hot_words}.')
	
	audio = sr.AudioData(frame_data, sample_rate, sample_width)
	try:
		transcript = recognizer.recognize_sphinx(
                audio, language=language, keyword_entries=hot_words)
		logger.debug(f'Transcript: {transcript}')
		return Response(transcript, 200)
	except sr.UnknownValueError:
		logger.debug(f'Uknown value')
		return Response('', 200)
	except Exception as err:
		logger.error(f'Error while recognizing. Error: {err}')
		return Response('', 500)

if(__name__ == '__main__'):
	app.run('0.0.0.0', port=5001)