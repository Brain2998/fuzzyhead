FROM alpine:3.9

COPY ./patator/requirements.txt requirements.txt

RUN apk add --no-cache --update python2 py-pip && \
    apk add --no-cache --virtual .build-dependencies build-base \
                       curl-dev \
                       mariadb-dev \
                       postgresql-dev \
                       python-dev \
                       libffi-dev && \
    pip install --upgrade --trusted-host pypi.python.org pip setuptools -r requirements.txt && \
    rm requirements.txt && \
    apk del .build-dependencies && \
    rm -r /root/.cache

WORKDIR /patator

ADD ./patator /patator

ENV NAME patator
