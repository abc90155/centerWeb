FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY . /docker_api/
RUN pip install --upgrade pip
RUN pip install Django
RUN pip install psycopg2-binary
RUN pip install whitenoise
