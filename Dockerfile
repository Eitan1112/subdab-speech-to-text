FROM ubuntu:18.04

RUN apt-get clean && apt-get update -y && \
    apt-get install -y nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools swig libasound2-dev libpulse-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

COPY nginx.conf /etc/nginx

# Download language models
RUN wget -O /usr/local/lib/python3.6/dist-packages/speech_recognition/pocketsphinx-data/pocketsphinx-data.tar https://storage.googleapis.com/pocketsphinx_languages/pocketsphinx-data.tar && \
    tar -xvf /usr/local/lib/python3.6/dist-packages/speech_recognition/pocketsphinx-data/pocketsphinx-data.tar

RUN chmod +x ./start.sh

CMD [ "./start.sh" ]