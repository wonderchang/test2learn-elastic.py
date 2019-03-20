

def test_same_doc_return_noop(es_master, create_index):
    index, doctype = create_index(), 'doc'

    doc1 = {'title': 'hi', 'content': 'yo'}
    doc2 = {'content': 'yoyo'}

    es_master.index(index, doctype, id=1, body=doc1, refresh=True)
    resp = es_master.update(
        index, 'doc', id=1, body={'doc': doc1}, refresh=True)
    assert resp == {
        'result': 'noop',
        '_index': index,
        '_type': 'doc',
        '_id': '1',
        '_version': 1,
        '_shards': {'failed': 0, 'successful': 0, 'total': 0},
    }

    resp = es_master.update(
        index, 'doc', id=1, body={'doc': doc2}, refresh=True)
    assert resp == {
        'result': 'updated',
        'forced_refresh': True,
        '_index': index,
        '_type': 'doc',
        '_id': '1',
        '_version': 2,
        '_primary_term': 1,
        '_seq_no': 1,
        '_shards': {'failed': 0, 'successful': 2, 'total': 2},
    }

    assert es_master.get(index, 'doc', id=1) == {
        'found': True,
        '_index': index,
        '_type': 'doc',
        '_id': '1',
        '_version': 2,
        '_source': {'title': 'hi', 'content': 'yoyo'}
    }


# vi:et:ts=4:sw=4:cc=80
