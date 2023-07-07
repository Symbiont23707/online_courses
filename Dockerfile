FROM python:3.10

COPY requirements.txt /temp/requirements.txt
COPY online_courses /online_courses
WORKDIR /online_courses

EXPOSE 8000

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user