FROM httpd:alpine

RUN apk add --no-cache bash apache2-ssl apache2-ldap
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/2 /var/log/apache2/error.log

COPY etc-httpd/ /usr/local/apache2/
COPY var-www-html/ /var/www/html/

# RUN chmod 777 /usr/local/apache2/logs

EXPOSE 80 443
