FROM python:3.5.2-alpine

COPY requirements.txt run.py /workdir/

RUN apk --no-cache add \
    gcc \
    musl-dev \
  && python3 -m pip install -r /workdir/requirements.txt \
  && adduser -D app \
  && mkdir -p /workdir  \
  && chown -R app:app /workdir

COPY flask_app /workdir/flask_app/

VOLUME /tmp

RUN chown -R app:app /workdir

WORKDIR /workdir

USER app

EXPOSE 8081

CMD ["python3", "run.py"]
