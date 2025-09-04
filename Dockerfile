FROM python:3.14.0rc2-alpine3.22

WORKDIR /app

ADD . .

#RUN python -m venv venv
RUN source venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]