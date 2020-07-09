FROM ubuntu:20.04

RUN apt-get clean && apt-get update -y && \
    apt-get install -y software-properties-common && \ 
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y nginx python3.8 python3-pip python3.8-dev build-essential libssl-dev libffi-dev python3-setuptools swig libasound2-dev libpulse-dev curl

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

COPY nginx.conf /etc/nginx

# Download language models
WORKDIR /usr/local/lib/python3.6/dist-packages/speech_recognition/pocketsphinx-data/
RUN curl https://storage.googleapis.com/pocketsphinx_languages/pocketsphinx-data.tar --output pocketsphinx-data.tar && \
    tar -xvf pocketsphinx-data.tar && \
    rm pocketsphinx-data.tar

WORKDIR /app

RUN chmod +x ./start.sh

CMD [ "./start.sh" ]