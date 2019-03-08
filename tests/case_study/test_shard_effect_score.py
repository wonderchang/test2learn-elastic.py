# https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch


def test_shared_effect_score(es_master, create_index):
    index = create_index()

    def add_index(id_, body):
        es_master.index(index, 'doc', id=id_, body=body, refresh=True)

    add_index('1', {'title': 'Shane'})
    add_index('2', {'title': 'Shane C'})
    add_index('3', {'title': 'Shane Connelly'})
    add_index('4', {'title': 'Shane P Connelly'})

    query = {"query": {"match": {"title": "Shane"}}}
    results = es_master.search(index, body=query)

    assert [(hit['_id'], hit['_score']) for hit in results['hits']['hits']] == [
        ('1', 0.2876821),
        ('3', 0.2876821),
        ('2', 0.19856805),
        ('4', 0.16853254),
    ]

    results = es_master.search(
        index, body=query, search_type='dfs_query_then_fetch')

    assert [(hit['_id'], hit['_score']) for hit in results['hits']['hits']] == [
        ('1', 0.13245322),
        ('2', 0.105360515),
        ('3', 0.105360515),
        ('4', 0.0874691),
    ]


# vi:et:ts=4:sw=4:cc=80
