############################
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add additional alpine download url in dockerfile
RUN echo -e "http://dl-4.alpinelinux.org/alpine/v3.12/main\nhttp://dl-4.alpinelinux.org/alpine/v3.12/community" > /etc/apk/repositories

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev mariadb-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/


# migrate
ENTRYPOINT ["sh", "/usr/src/entrypoint.sh"]