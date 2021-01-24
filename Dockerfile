FROM python:3.8 

RUN apt update
RUN pip install pyyaml python-digitalocean boto3
RUN mkdir /code
WORKDIR /code