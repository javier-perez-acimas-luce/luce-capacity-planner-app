FROM python:3.10-slim
LABEL maintainer="Luce Innovative Technologies"

EXPOSE 8080

ENV PORT="8080"
ENV HOST="0.0.0.0"
ENV LOGLEVEL=INFO

WORKDIR /app
COPY src .

RUN apt update && apt upgrade -y && apt install -y build-essential \
    && pip install -r requirements.txt \
    && apt remove -y build-essential \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r luceit && adduser --system --no-create-home luceit \
    && chown -R luceit:luceit /app

USER luceit

CMD exec gunicorn --bind $HOST:$PORT --workers 1 --threads 8 --timeout 0 --log-level=$LOGLEVEL main:app --chdir app_name