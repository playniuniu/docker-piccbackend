FROM alpine:latest
MAINTAINER playniuniu@gmail.com

COPY app/ /usr/src/app
WORKDIR /usr/src/app

RUN apk add --no-cache --update python3 \
    && pyvenv /env \
    && /env/bin/pip install --no-cache-dir -r /usr/src/app/requirements.txt \
    && rm -rf /var/cache/apk/*

VOLUME /data
EXPOSE 4000

CMD ["/env/bin/gunicorn", "-b", "0.0.0.0:4000", "server:app"]
