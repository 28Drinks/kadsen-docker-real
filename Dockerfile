FROM ubuntu:20.04  

ENV DEBIAN_FRONTEND nointeractive

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# ENTRYPOINT [ "python3" ]

CMD ["python3", "-u", "app.py"]
