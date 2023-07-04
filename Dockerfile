FROM python:3.11-slim-buster

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app
WORKDIR /app/tgbot

CMD ["gunicorn", "tgbot.wsgi:application", "--bind", "0:8000" ]
