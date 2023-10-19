FROM python:3.9.15-slim-bullseye

RUN apt update && apt install default-libmysqlclient-dev build-essential libtk nodejs npm pkg-config -y

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN npm i -g nodemon

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

COPY index.py index.py
COPY dbutils.py dbutils.py
ADD core core
ADD titles titles
ADD config config
ADD logs logs
ADD cert cert

ENTRYPOINT [ "/app/entrypoint.sh" ]