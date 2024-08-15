FROM --platform=linux/amd64 python:3.12.4-bullseye

WORKDIR /app

COPY . /app

ENV CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHON_ENV="production"

CMD ["python", "main.py"]
