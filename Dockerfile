FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
