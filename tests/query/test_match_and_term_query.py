# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.htm


def test_match_and_term_query(es_master, create_index):
    index = create_index(body={
        "settings": {
            "number_of_shards": 1,
        },
        "mappings": {
            "doc": {
                "properties": {
                    "full_text": {
                        "type":  "text",
                    },
                    "exact_value": {
                        "type":  "keyword",
                    },
                },
            },
        },
    })
    es_master.index(index, 'doc', id=1, body={
        "full_text": "Quick Foxes!",
        "exact_value": "Quick Foxes!",
    }, refresh=True)

    def searchable(body):
        return es_master.search(index, body=body)['hits']['total'] == 1

    assert not searchable({"query": {"term": {"exact_value": "Quick Foxes"}}})
    assert not searchable({"query": {"term": {"exact_value": "quick foxes!"}}})
    assert searchable({"query": {"term": {"exact_value": "Quick Foxes!"}}})

    assert not searchable({"query": {"term": {"full_text": "Quick Foxes!"}}})   # useless
    assert searchable({"query": {"term": {"full_text": "foxes"}}})

    assert searchable({"query": {"match": {"full_text": "Quick Foxes!"}}})
    assert searchable({"query": {"match": {"full_text": "quick"}}})
    assert searchable({"query": {"match": {"full_text": "foxes"}}})


# vi:et:ts=4:sw=4:cc=80
