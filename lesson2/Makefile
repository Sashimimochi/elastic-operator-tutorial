delete:
	kind delete cluster

apply:
	kubectl apply -f manifest/

setup:
	@make delete
	kind create cluster
	docker build -t python-web-app:1.2 .
	kind load docker-image python-web-app:1.2
	@make apply

test:
	docker run --rm -it -v `pwd`:/bzt-configs blazemeter/taurus:latest test.yaml
