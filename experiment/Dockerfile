###########
# BUILDER #
###########

# pull official base image
FROM python:3.8-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install SO dependencies
RUN apt-get update
RUN apt-get install -y build-essential python3-dev default-libmysqlclient-dev

RUN pip install --upgrade pip
COPY . /usr/src/app/

# install dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN groupadd -g 10001 app
RUN useradd -u 10002 -g 10001 app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

RUN apt-get update --fix-missing & apt-get install -y netcat-openbsd libmariadb-dev

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run migrations
#RUN python manage.py flush --no-input
#RUN python manage.py migrate

# add execution permission
RUN chmod +x $APP_HOME/entrypoint.sh

ENTRYPOINT ["/home/app/web/entrypoint.sh"]