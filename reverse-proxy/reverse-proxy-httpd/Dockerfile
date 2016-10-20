FROM httpd:alpine

RUN apk add --no-cache bash apache2-ssl apache2-ldap

# RUN yum -y update \
#     && yum -y install httpd mod_ssl mod_ldap \
#     && yum -y clean all

# COPY httpd-foreground /usr/local/bin/
COPY etc-httpd/ /usr/local/apache2/
COPY var-www-html/ /var/www/html/

# RUN chmod +x /usr/local/bin/httpd-foreground

EXPOSE 80 443

CMD ["httpd-foreground"]