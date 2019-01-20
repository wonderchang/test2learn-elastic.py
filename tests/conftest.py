import os
import uuid

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

@pytest.fixture
def create_index(es_master):
    indexes = []
    def _create_index(body=None):
        index = uuid.uuid4().hex
        es_master.indices.create(index, body)
        indexes.append(index)
        return index

    yield _create_index
    for index in indexes:
        es_master.indices.delete(index)

@pytest.fixture
def assert_token_analyze(es_master, create_index):
    def _assert_token_analyze(analyze, tokens, settings=None):
        index = create_index(settings)
        data = es_master.indices.analyze(index, analyze)
        assert [token['token'] for token in data['tokens']] == tokens

    return _assert_token_analyze


# vi:et:ts=4:sw=4:cc=80
