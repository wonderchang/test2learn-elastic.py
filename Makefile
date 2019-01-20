TEST ?=
test_image = learning-elasticsearch
test_workspace = /workspace

es_version = 6.5.4
es_image_name = docker.elastic.co/elasticsearch/elasticsearch

export ES_IMAGE = $(es_image_name):$(es_version)
export ES_NETWORK = es-network

export ES_MASTER_CLUSTER = es-master
export ES_DEFAULT_PORT = 9200

export ES_MASTER_N1_NAME = $(ES_MASTER_CLUSTER)-n1
export ES_MASTER_N1_HOST = $(ES_MASTER_N1_NAME):$(ES_DEFAULT_PORT)
export ES_MASTER_N1_PUBLISH_PORT = 9200

export ES_MASTER_N2_NAME = $(ES_MASTER_CLUSTER)-n2
export ES_MASTER_N2_HOST = $(ES_MASTER_N2_NAME):$(ES_DEFAULT_PORT)
export ES_MASTER_N2_PUBLISH_PORT = 9201

export ES_REPLICA_CLUSTER = es-replica

export ES_REPLICA_N1_NAME = $(ES_REPLICA_CLUSTER)-n1
export ES_REPLICA_N1_HOST = $(ES_REPLICA_N1_NAME):$(ES_DEFAULT_PORT)
export ES_REPLICA_N1_PUBLISH_PORT = 9210

export ES_REPLICA_N2_NAME = $(ES_REPLICA_CLUSTER)-n2
export ES_REPLICA_N2_HOST = $(ES_REPLICA_N2_NAME):$(ES_DEFAULT_PORT)
export ES_REPLICA_N2_PUBLISH_PORT = 9211

docker_run_opts = --rm --tty \
				  --workdir $(test_workspace) \
				  --volume $(PWD):$(test_workspace) \
				  --network $(ES_NETWORK) \

define docker_run
	docker run $(docker_run_opts) $(test_image) $(1)
endef

build: image elasticsearch

image:
	docker build -t $(test_image) .

elasticsearch:
	docker-compose up -d

test: docker_run_opts += --env ES_MASTER_N1_HOST=$(ES_MASTER_N1_HOST)
test: docker_run_opts += --env ES_MASTER_N2_HOST=$(ES_MASTER_N2_HOST)
test: docker_run_opts += --env ES_REPLICA_N1_HOST=$(ES_REPLICA_N1_HOST)
test: docker_run_opts += --env ES_REPLICA_N2_HOST=$(ES_REPLICA_N2_HOST)
test:
	$(call docker_run,pytest -vvv $(TEST))

shell: docker_run_opts += --interactive
shell:
	$(call docker_run,/bin/bash)

clean:
	docker-compose down -v
	docker rmi -f $(test_image)


# vi:ts=4:sw=4:cc=80
