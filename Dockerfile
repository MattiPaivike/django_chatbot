FROM ubuntu:22.04

COPY ./scripts/gunicorn/run.sh /scripts/run.sh
COPY ./scripts/gunicorn/gunicorn_config.py /scripts/gunicorn_config.py
COPY ./django_chatbot_app /app
COPY ./requirements_prod.txt /app/requirements.txt

WORKDIR /app
EXPOSE 9000

RUN apt-get update && \
    apt-get -y install libpq-dev gcc python3 python3-pip python3.10-venv && \
    python3 -m venv /py && \
    /py/bin/pip3 install --upgrade pip && \
    /py/bin/pip3 install -r requirements.txt && \
    adduser --disabled-password --no-create-home --gecos '' app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/logging && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Update package lists, upgrade packages, and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

VOLUME /vol/web

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
