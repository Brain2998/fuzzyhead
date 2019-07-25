FROM alpine:3.9

WORKDIR /app

COPY . /app

RUN apk add --no-cache --update python3 py3-pip && \
    pip3 install --upgrade flask

EXPOSE 5000

CMD ["python3", "upload.py"]
