FROM --platform=linux/amd64 python:3.12.4-bullseye AS build_amd64

WORKDIR /app

COPY . /app

ENV CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"

RUN pip install --upgrade pip && pip install -r requirements/prod.txt

ENV PYTHON_ENV="production"
ENV PORT=80

CMD ["python", "main.py"]
