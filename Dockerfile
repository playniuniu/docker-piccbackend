FROM alpine:latest
MAINTAINER playniuniu@gmail.com

COPY . /usr/src/
WORKDIR /usr/src/

RUN apk add --no-cache --update python3 \
    && pyvenv /env \
    && /env/bin/pip install --no-cache-dir -r /usr/src/requirements.txt \
    && rm -rf /var/cache/apk/*

VOLUME /data
EXPOSE 4000

CMD ["/env/bin/gunicorn", "-b", "0.0.0.0:4000", "app:app"]
