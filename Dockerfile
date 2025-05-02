FROM python:3.9.16

RUN mkdir /app

WORKDIR /app

RUN pip install "pip==23.3"
RUN pip install "sqlalchemy>=2.0.0"
RUN pip install "psycopg2"

COPY main.py /app/

