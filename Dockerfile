FROM python:3.6
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
