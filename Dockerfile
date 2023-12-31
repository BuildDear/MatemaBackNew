# pull the official base image
FROM python:3.10.13-bullseye

#RUN apt-get update && apt-get install -y mysql-client
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app
# Копіювання скрипту entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Надання прав на виконання скрипту
RUN chmod +x /usr/src/app/entrypoint.sh

# Встановлення скрипту як точки входу
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Відкриття порту 8000
EXPOSE 8000
