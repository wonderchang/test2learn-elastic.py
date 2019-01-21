import pytest


def test_create_and_restore_to_replica_cluster(
        es_master, es_replica, create_index, create_repo):
    repo = create_repo()

    index = create_index()
    doc_type = '_doc'
    source1= {'title': 'Hi', 'content': 'No more'}
    source2 = {'title': 'Hey', 'content': 'Nothing'}
    es_master.index(index, doc_type, source1, id='1', refresh='true')
    es_master.index(index, doc_type, source2, id='2', refresh='true')

    es_master.snapshot.create(repo, "doc-snapshot1", {
        "indices": index,
        "ignore_unavailable": True,
        "include_global_state": False,
    }, wait_for_completion=True)

    es_replica.snapshot.restore(repo, "doc-snapshot1", {
        "indices": index,
        "ignore_unavailable": True,
        "include_global_state": True,
    }, wait_for_completion=True)

    result = es_replica.mget({"ids": ["1", "2"]}, index)
    docs = result['docs']

    assert len(docs) ==2
    assert docs[0]['_index'] == index
    assert docs[0]['_source'] == source1
    assert docs[1]['_index'] == index
    assert docs[1]['_source'] == source2


# vi:et:ts=4:sw=4:cc=80
