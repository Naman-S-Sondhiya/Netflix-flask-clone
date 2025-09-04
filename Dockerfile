FROM python:3.12-slim

WORKDIR /app

ADD . .

RUN python -m venv venv 

RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

EXPOSE 5000

CMD ["/app/venv/vin/python", "app.py"]