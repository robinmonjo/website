FROM --platform=linux/amd64 python:3.12.4-bookworm AS build_amd64

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --upgrade uv && \
    uv sync --no-dev

CMD ["bash", "docker_start.sh"]
