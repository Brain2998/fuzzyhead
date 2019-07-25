FROM alpine:3.9

RUN apk update && apk add --no-cache --update python3 && \
    pip3 install --no-cache-dir celery docker

RUN apk add --no-cache tzdata && \ 
	cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \ 
        echo "Europe/Moscow" > /etc/timezone && touch /tmp/result.txt && touch /tmp/wordlist.txt

ENV NAME worker

WORKDIR /

COPY ./fuzzyhead /fuzzyhead

CMD celery -A fuzzyhead worker --loglevel=info --concurrency 1
