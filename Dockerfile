FROM python:3.11
RUN apt update; apt upgrade -y; apt install -y openssh-client
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
CMD /app/init.sh
