FROM python:3.12-slim

WORKDIR /app

ADD . .

RUN python -m venv venv 

RUN source /venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]