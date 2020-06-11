from flask import Flask, request, Response
import speech_recognition as sr
import base64
import logging

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

@app.route('/Convert', methods=['POST', 'GET'])
def convert():
	language = request.form['language'] 
	hot_word = request.form['hot_word']
	recognizer = sr.Recognizer()
	frame_data_base64 = request.form['frame_data_base64']
	frame_data = base64.b64decode(frame_data_base64)
	sample_rate = int(request.form['sample_rate'])
	sample_width = int(request.form['sample_width'])

	logger.debug(f'Recieved request. Language: {language}. Hot word: {hot_word}.')
	
	audio = sr.AudioData(frame_data, sample_rate, sample_width)
	try:
		transcript = recognizer.recognize_sphinx(
                audio, language=language, keyword_entries=[(hot_word, 1)])
		logger.debug(f'Transcript: {transcript}')
		return Response(transcript, 200)
	except sr.UnknownValueError:
		logger.debug(f'Uknown value')
		return Response('', 200)
	except Exception as err:
		logger.error(f'Error while recognizing. Error: {err}')
		return Response('', 500)
