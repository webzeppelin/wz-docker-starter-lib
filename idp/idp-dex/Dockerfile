FROM golang:alpine

RUN echo "Dockerfile -> Downloading and building stable version of dex..." \
    && apk --no-cache add bash curl tar git gcc musl-dev \
    && mkdir /build \
    && cd /build \
    && curl -fsSL "https://github.com/coreos/dex/archive/v0.6.1.tar.gz" | tar -xzC "/build" --strip-components=1 \
	&& ./build \
	&& mkdir -p /opt/dex/bin \
	&& cp bin/dex-worker /opt/dex/bin/dex-worker \
	&& cp bin/dex-overlord /opt/dex/bin/dex-overlord \
	&& cp bin/dexctl /opt/dex/bin/dexctl

COPY static /opt/dex/static/

# COPY static/fixtures/emailer.json /opt/dex/email/emailer.json
COPY docker_entry_command.sh /opt/dex/docker_entry_command.sh
COPY env.sh /opt/dex/env.sh

RUN echo "Dockerfile -> Cleaning up build environment..." \
    && rm -rf /build \
    && apk del git gcc musl-dev

WORKDIR /opt/dex

EXPOSE 5555 5556 5557

CMD ["/bin/bash","/opt/dex/docker_entry_command.sh"]
