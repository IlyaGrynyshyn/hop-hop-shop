FROM python:3.10.9-slim-buster
LABEL authors="Ilya_Grynyshyn"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/app
RUN chmod +x /usr/src/app/scripts/run.sh

CMD ["/usr/src/app/scripts/run.sh"]



