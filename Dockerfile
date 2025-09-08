FROM python:3.12-slim

WORKDIR /app

ADD . .

ARG TMDB_API_KEY

ENV TMDB_API_KEY=$TMDB_API_KEY

RUN python -m venv venv 

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

EXPOSE 5000

CMD ["/app/venv/bin/python", "app.py"]