FROM redis:alpine

RUN apk add --no-cache bash

COPY redis.conf /home/redis/redis.conf

CMD [ "redis-server", "/home/redis/redis.conf" ]
