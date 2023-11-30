FROM python:latest

WORKDIR /app

COPY Scripts /app/Scripts

WORKDIR /app/Scripts

COPY requirements.txt /app/Scripts/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]