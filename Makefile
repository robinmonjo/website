lint:
	black . && pylint --recursive=y .

build:
	docker build -t website:latest .

push:
	docker tag website:latest robinmonjo/website:latest && docker push robinmonjo/website:latest
