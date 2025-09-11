FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r requirements.txt

COPY . .

ARG TMDB_API_KEY

ENV TMDB_API_KEY=$TMDB_API_KEY

EXPOSE 5000

CMD ["/app/venv/bin/python", "app.py"]