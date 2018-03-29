CONTAINER_NAME=foreman-stub
IMAGE_NAME=foreman-simulator

.PHONY: all
all: build
	docker run -it --rm --name ${CONTAINER_NAME} -p8080:8080 ${IMAGE_NAME}

.PHONY: build
build:
	docker build -t ${IMAGE_NAME} .

.PHONY: dev
dev: build
	docker run -it --rm --name ${CONTAINER_NAME} -p8080:8080 -v "`pwd`:/usr/src/app" -e DEBUG=1 ${IMAGE_NAME}
