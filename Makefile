.PHONY: all
all: build
	docker run -it --rm --name foreman_stub -p8080:8080 foreman_stub

.PHONY: build
build:
	docker build -t foreman_stub .

.PHONY: dev
dev: build
	docker run -it --rm --name foreman_stub -p8080:8080 -v "`pwd`:/usr/src/app" -e DEBUG=1 foreman_stub
