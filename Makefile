lint:
	black . && pylint --recursive=y .

build:
	docker build --network=host -t website:latest .

push:
	docker tag website:latest robinmonjo/website:latest && docker push robinmonjo/website:latest

prod-run:
	docker run -d --restart unless-stopped -p 80:80 -e LLAMA_VERBOSE=true --ulimit memlock=-1:-1 website

remote-build: export DOCKER_HOST=ssh://root@[2a01:4f8:1c1c:f9c4::1]
remote-build: build

start-llm:
	python -m llama_cpp.server --model=models/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf --n_ctx=4096 --cache true
