FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt-get install -y gpac
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
