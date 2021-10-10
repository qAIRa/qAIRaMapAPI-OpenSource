FROM python:3.8.12-bullseye

ENV PYTHONUNBUFFERED=1
ENV SQLALCHEMY_DATABASE_URI_OPEN='postgres://postgres:postgres@test_database:5432/postgres'

WORKDIR /src

COPY requirements.txt /src/
COPY requirements_test.txt /src/

RUN pip install -r requirements.txt -r requirements_test.txt
