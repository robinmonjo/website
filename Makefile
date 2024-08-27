lint:
	black . && pylint --recursive=y .

build:
	docker build --network=host -t website:latest .

push:
	docker tag website:latest robinmonjo/website:latest && docker push robinmonjo/website:latest

prod-run:
	docker run -d --restart unless-stopped -p 80:80 --ulimit memlock=-1:-1 website

remote-build: export DOCKER_HOST=ssh://root@[2a01:4f8:1c1b:b920::1]
remote-build: build

MODEL := Phi-3.1-mini-4k-instruct-Q4_K_M.gguf

serve-llm:
	python -m llama_cpp.server --model=models/${MODEL} --n_ctx=4096

UNAME := $(shell uname -s)

ifeq ($(UNAME), Linux)
	LLAMA_SERVER = llm/llama-server-linux
else ifeq ($(UNAME), Darwin)
	LLAMA_SERVER = llm/llama-server-macos
endif

serve-llm2:
	./$(LLAMA_SERVER) -m models/${MODEL} --host 0.0.0.0 --port 8000 -cnv --mlock --log-disable
