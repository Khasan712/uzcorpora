FROM python:3.11

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /uzcorpora
WORKDIR /uzcorpora
RUN pip install --upgrade pip && pip install -r requirements.txt
