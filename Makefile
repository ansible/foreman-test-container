.PHONY: all
all: build
	docker run -it --rm --name foreman-simulator -p8080:8080 foreman-simulator

.PHONY: build
build:
	docker build -t foreman-simulator .

.PHONY: dev
dev: build
	docker run -it --rm --name foreman-simulator -p8080:8080 -v "`pwd`:/usr/src/app" -e DEBUG=1 foreman-simulator
