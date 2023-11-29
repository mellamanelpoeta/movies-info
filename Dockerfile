FROM python:latest
WORKDIR /Scripts
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000