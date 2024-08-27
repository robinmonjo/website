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

serve-llm:
	python -m llama_cpp.server --model=models/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf --n_ctx=4096

serve-llm2:
	./llm/llama-server -m models/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf --host 0.0.0.0 --port 8000 -cnv --mlock
