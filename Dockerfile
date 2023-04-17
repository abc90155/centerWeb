FROM python:3.9
LABEL MAINTAINER KPY
ENV PYTHONUNBUFFERED 1
RUN mkdir /centerWeb
WORKDIR /centerWeb
COPY . /centerWeb/
RUN pip install -r requirements.txt