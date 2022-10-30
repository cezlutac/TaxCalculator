FROM python:3.8-slim

ENV APP_GROUP=app \
    APP_USER=app

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update \
    && apt-get install -qq ca-certificates gettext git libxmlsec1-dev gcc gnupg2 libpq-dev \
    && pip install 'pipenv>=8.3.0,<8.4.0' \
    && groupadd ${APP_GROUP} \
    && useradd -m -g ${APP_GROUP} ${APP_USER} \
    && echo -n "America/Toronto" > /etc/timezone

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN sed -i -e 's/localhost/host.docker.internal/g' *.py

COPY ["Pipfile.lock", "/tmp/"]

RUN cd /tmp \
    && pipenv install --ignore-pipfile --dev --system

EXPOSE 4000

CMD gunicorn app:app -w 2 -b :4000 \
    --access-logfile acces.log --error-logfile error.log