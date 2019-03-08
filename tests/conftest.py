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
    def _create_index(index=None, body=None):
        if not index:
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
        index = create_index(body=settings)
        data = es_master.indices.analyze(index, analyze)
        assert [token['token'] for token in data['tokens']] == tokens

    return _assert_token_analyze

@pytest.fixture
def create_repo(es_master, es_replica):
    repos = []
    def _create_repo(repo=None):
        if not repo:
            repo = uuid.uuid4().hex

        body = {
            "type": "fs",
            "settings": {
                "location": os.environ.get("ES_REPO_PATH"),
            }
        }
        es_master.snapshot.create_repository(repo, body=body)
        es_replica.snapshot.create_repository(repo, body=body)
        repos.append(repo)

        return repo

    yield _create_repo

    for repo in repos:
        snapshots = es_master.snapshot.get(repo, '_all')
        for snapshot in snapshots['snapshots']:
            es_master.snapshot.delete(repo, snapshot['snapshot'])

        snapshots = es_replica.snapshot.get(repo, '_all')
        for snapshot in snapshots['snapshots']:
            es_replica.snapshot.delete(repo, snapshot['snapshot'])

        es_master.snapshot.delete_repository(repo)
        es_replica.snapshot.delete_repository(repo)

@pytest.fixture
def set_index_template(es_master):
    templates = []

    def _set_index_template(template_body):
        template = uuid.uuid4().hex
        es_master.indices.put_template(template, template_body)
        templates.append(template)

    yield _set_index_template

    for template in templates:
        es_master.indices.delete_template(template)


# vi:et:ts=4:sw=4:cc=80
