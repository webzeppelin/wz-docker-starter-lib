FROM httpd:alpine

RUN apk add --no-cache bash apache2-ssl apache2-ldap

COPY etc-httpd/ /usr/local/apache2/
COPY var-www-html/ /var/www/html/

RUN chmod 777 /usr/local/apache2/logs

EXPOSE 80 443
