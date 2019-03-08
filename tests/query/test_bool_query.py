

def test_bool_query(es_master, create_index):
    index = create_index()

    def add_index(id_, body):
        es_master.index(index, 'doc', id=id_, body=body, refresh=True)

    add_index('1', {'title': 'Shane'})
    add_index('2', {'title': 'Shane C'})
    add_index('3', {'title': 'Shane Connelly'})
    add_index('4', {'title': 'Shane P Connelly'})

    query_body = {
        'query': {
            'bool': {
                'must': {
                    'match': {'title': 'Connelly'},
                },
            },
        },
    }
    results = es_master.search(
        index, body=query_body, search_type='dfs_query_then_fetch')

    assert [(hit['_id'], hit['_score']) for hit in results['hits']['hits']] == [
        ('3', 0.6931472),
        ('4', 0.5754429),
    ]



# vi:et:ts=4:sw=4:cc=80
