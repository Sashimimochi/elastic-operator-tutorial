SHELL := /bin/bash
.ONSHELL:

MONITOR_NAMESPACE=monitoring
PROM_OPER_REL=mon
ELASTIC_NAMESPACE="elastic-system"
ELASTICSEARC_ENDPOINT=http://elastic.local
ELASTIC_OPERATOR_VERSION=2.14.0

operator:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	kubectl wait --namespace ingress-nginx \
  --for=condition=available \
	deployment.apps/ingress-nginx-controller \
  --timeout=90s
	sleep 10
	kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
	helm install elastic-operator elastic/eck-operator -n $(ELASTIC_NAMESPACE) --create-namespace --version $(ELASTIC_OPERATOR_VERSION)
	kubectl wait --namespace $(ELASTIC_NAMESPACE) \
  --for=condition=ready \
	pod/elastic-operator-0 \
  --timeout=90s

monitoring:
# Prometheusなどのインストール
	helm upgrade --install $(PROM_OPER_REL) prometheus-community/kube-prometheus-stack \
	--namespace $(MONITOR_NAMESPACE) \
	--create-namespace \
	--set kubeStateMetrics.enabled=true \
	--set nodeExporter.enabled=true

del-operator:
	helm delete elastic-operator -n $(ELASTIC_NAMESPACE)

apply:
	helm install fluentd fluent/fluentd -f fluent-values.yaml
	kubectl apply -f manifest/
	sleep 60
	kubectl wait --namespace $(ELASTIC_NAMESPACE) \
  --for=condition=ready \
	pod/quickstart-es-default-0 \
  --timeout=600s
	helm install elastic-exporter prometheus-community/prometheus-elasticsearch-exporter -f elastic-exporter-values.yaml -n $(ELASTIC_NAMESPACE)

delete:
	kubectl delete -f manifest/
	helm uninstall elastic-exporter

start:
	kind create cluster --config cluster.yaml

down:
	kind delete cluster

health: password healthcheck
run: password add-index get-index

password:
	$(eval PASSWORD=`kubectl get secret quickstart-es-elastic-user -n $(ELASTIC_NAMESPACE) -o go-template='{{.data.elastic | base64decode}}'`)
	echo $(PASSWORD)

healthcheck:
	curl -u "elastic:$(PASSWORD)" -k "$(ELASTICSEARC_ENDPOINT)/_cluster/health?pretty"

create-index:
	curl -u "elastic:$(PASSWORD)" -X PUT -k "$(ELASTICSEARC_ENDPOINT)/products?pretty"

add-index:
	curl -u "elastic:$(PASSWORD)" -X POST -k "$(ELASTICSEARC_ENDPOINT)/_bulk?pretty" -H 'Content-Type: application/json' --data-binary @data.json

get-index:
	curl -u "elastic:$(PASSWORD)" -X GET -k "$(ELASTICSEARC_ENDPOINT)/products/_search?q=name:Elasticsearch&pretty"

setup:
	helm repo add elastic https://helm.elastic.co
	helm repo add fluent https://fluent.github.io/helm-charts
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add stable https://charts.helm.sh/stable
	helm repo update

clean:
	@make down
	helm repo remove elastic fluent prometheus-community stable

up:
	@make down
	@make start
	@make operator
	@make monitoring
	@make apply
	@make health
	@make run
