import os
import pytest

from elasticsearch import Elasticsearch


@pytest.fixture(scope='session')
def es_master():
    n1_host = 'http://' + os.environ.get('ES_MASTER_N1_HOST')
    n2_host = 'http://' + os.environ.get('ES_MASTER_N2_HOST')

    return Elasticsearch([n1_host, n2_host])

@pytest.fixture(scope='session')
def es_replica():
    n1_host = 'http://' + os.environ.get('ES_REPLICA_N1_HOST')
    n2_host = 'http://' + os.environ.get('ES_REPLICA_N2_HOST')

    return Elasticsearch([n1_host, n2_host])


# vi:et:ts=4:sw=4:cc=80
