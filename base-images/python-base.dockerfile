# FROM ubuntu:18.04
FROM python:3.5-alpine


# RUN apt update && apt install python3 python3-pip -y
RUN pip3 install pika
RUN pip3 install nltk
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader vader_lexicon
