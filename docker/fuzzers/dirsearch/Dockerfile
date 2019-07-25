FROM alpine:3.9

WORKDIR /dirsearch

COPY ./dirsearch /dirsearch

RUN apk update && apk add --no-cache --update python3

ENV NAME dirsearch
