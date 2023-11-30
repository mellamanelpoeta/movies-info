FROM python:3.9.18-slim

WORKDIR /app

COPY Scripts /app/Scripts

WORKDIR /app/Scripts

COPY requirements.txt /app/Scripts/
RUN pip install -r requirements.txt

CMD ["python", "main.py"]