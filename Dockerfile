FROM python:3.11

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /uzcorpora
WORKDIR /uzcorpora
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#RUN adduser uzcorpora_user
#RUN chown -R uzcorpora_user:uzcorpora_user /uzcorpora
#RUN chmod -R 777 /uzcorpora/entrypoint.sh
#USER uzcorpora_user

