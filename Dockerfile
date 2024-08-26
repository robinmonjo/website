FROM --platform=linux/amd64 python:3.12.4-bullseye AS build_amd64

WORKDIR /app

COPY . /app

ENV CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"

RUN pip install --upgrade pip && pip install -r requirements/prod.txt

CMD ["bash", "docker_start.sh"]
