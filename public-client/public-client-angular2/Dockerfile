FROM nginx:stable-alpine

RUN apk add --no-cache bash nodejs make g++ python
# RUN npm install webpack -g

COPY package.json /tmp/build/package.json
RUN cd /tmp/build && npm install
# RUN mkdir -p /opt/app && cp -a /tmp/node_modules /opt/app/

COPY . /tmp/build
RUN cd /tmp/build && \
    npm run build && \
    cp -a dist/* /usr/share/nginx/html/

RUN cd /tmp/build && \
    cp etc-nginx/nginx.conf /etc/nginx/ && \
    cp etc-nginx/conf.d/*.conf /etc/nginx/conf.d/ && \
    rm /etc/nginx/conf.d/default.conf && \
    cp etc-ssl/* /etc/ssl/ && \
    cd / && \
    rm -rf /tmp/build

RUN apk del nodejs make g++ python

EXPOSE 80 443
