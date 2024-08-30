lint:
	uv run black . && uv run pylint --recursive=y .

SERVER_IP := 2a01:4f8:1c1c:8d49::1
COUNTAINER_NAME := website

export DOCKER_HOST=ssh://root@[${SERVER_IP}]

build:
	docker build --network=host -t website:latest .

run:
	docker run --name ${COUNTAINER_NAME} -d --restart unless-stopped -p 8080:80 --ulimit memlock=-1:-1 website

stop:
	docker stop ${COUNTAINER_NAME} || true
	docker rm ${COUNTAINER_NAME} || true

deploy: build stop run

MODEL := Phi-3.1-mini-4k-instruct-Q4_K_M.gguf
UNAME := $(shell uname -s)

ifeq ($(UNAME), Linux)
	LLAMA_SERVER = llm/llama-server-linux
else ifeq ($(UNAME), Darwin)
	LLAMA_SERVER = llm/llama-server-macos
endif

serve-llm:
	./$(LLAMA_SERVER) -m models/${MODEL} --host 127.0.0.1 --port 8000 -cnv --mlock --log-disable
