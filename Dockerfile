FROM python:3.11
RUN apt update; apt upgrade -y; apt install -y openssh-client
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD init.sh
