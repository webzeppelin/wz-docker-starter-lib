#!/bin/bash

openssl genrsa -out domain.key 2048
openssl req -x509 -new -nodes -key domain.key -sha256 -days 1024 -out domain.pem -subj "/C=US/ST=TX/L=Austin/O=Webzeppelin Enterprises/OU=DEVOPS/CN=wzstarter.org"
openssl x509 -outform der -in domain.pem -out domain.crt

openssl genrsa -out generic.key 2048
openssl req -new -key generic.key -out generic.csr -subj "/C=US/ST=TX/L=Austin/O=Webzeppelin Enterprises/OU=DEVOPS/CN=generic.wzstarter.org"
openssl x509 -req -in generic.csr -CA domain.pem -CAkey domain.key -CAcreateserial -out generic.crt -days 1000 -sha256

openssl genrsa -out idp.key 2048
openssl req -new -key idp.key -out idp.csr -subj "/C=US/ST=TX/L=Austin/O=Webzeppelin Enterprises/OU=DEVOPS/CN=idp.wzstarter.org"
openssl x509 -req -in idp.csr -CA domain.pem -CAkey domain.key -CAcreateserial -out idp.crt -days 1000 -sha256

openssl genrsa -out app.key 2048
openssl req -new -key app.key -out app.csr -subj "/C=US/ST=TX/L=Austin/O=Webzeppelin Enterprises/OU=DEVOPS/CN=app.wzstarter.org"
openssl x509 -req -in app.csr -CA domain.pem -CAkey domain.key -CAcreateserial -out app.crt -days 1000 -sha256

openssl genrsa -out admin.key 2048
openssl req -new -key admin.key -out admin.csr -subj "/C=US/ST=TX/L=Austin/O=Webzeppelin Enterprises/OU=DEVOPS/CN=admin.wzstarter.org"
openssl x509 -req -in admin.csr -CA domain.pem -CAkey domain.key -CAcreateserial -out admin.crt -days 1000 -sha256

rm *.csr
rm *.srl
