FROM python:3.10.6-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ Asia/Seoul

RUN apt update -y
RUN apt upgrade -y

COPY . /api
WORKDIR /api

RUN rm -rf venv
RUN rm -rf log
RUN rm -rf tmp
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["sh", "bin/run.sh"]