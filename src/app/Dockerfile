
# pull the official docker image
FROM python:3.8

# set work directory
WORKDIR /app


# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get install ffmpeg libsm6 libxext6  -y
