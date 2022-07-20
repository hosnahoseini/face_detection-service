FROM python:3.8

RUN mkdir -p /home/app


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r /home/app/requirements.txt

COPY . /home/app

EXPOSE 8001
CMD ["python", "/home/app/main.py"] 
