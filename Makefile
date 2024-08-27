lint:
	black . && pylint --recursive=y .

SERVER_IP := 2a01:4f9:c012:eab9::1

export DOCKER_HOST=ssh://root@[${SERVER_IP}]

build:
	docker build --network=host -t website:latest .

run:
	docker run -d --restart unless-stopped -p 80:80 --ulimit memlock=-1:-1 website

MODEL := Phi-3.1-mini-4k-instruct-Q4_K_M.gguf
UNAME := $(shell uname -s)

ifeq ($(UNAME), Linux)
	LLAMA_SERVER = llm/llama-server-linux
else ifeq ($(UNAME), Darwin)
	LLAMA_SERVER = llm/llama-server-macos
endif

serve-llm:
	./$(LLAMA_SERVER) -m models/${MODEL} --host 0.0.0.0 --port 8000 -cnv --mlock --log-disable
