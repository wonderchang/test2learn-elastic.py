import pytest

from tests.helper import get_hit_doc_id_and_score


@pytest.fixture
def index(es_master, create_index, set_index_template):
    set_index_template({
        'index_patterns': ['*'],
        'settings': {'number_of_shards': 1},
    })
    index = create_index()

    def add_index(id_, body):
        es_master.index(index, 'doc', id=id_, body=body, refresh=True)

    add_index('1', {'title': 'Shane', 'intro': 'is my best friend'})
    add_index('2', {'title': 'Shane C', 'intro': 'who borned in 1999'})
    add_index('3', {'title': 'Shane Connelly', 'intro': 'from UK'})
    add_index('4', {'title': 'Shane P Connelly', 'intro': 'software engineer'})

    return index

def test_query_simple_match(es_master, index):
    assert get_hit_doc_id_and_score(es_master.search(index, body={
        'query': {
            'match': {
                'title': 'Connelly',
            },
        },
    })) == [
        ('3', 0.6931472),
        ('4', 0.5754429),
    ]

    assert get_hit_doc_id_and_score(es_master.search(index, body={
        'query': {
            'match_all': {},
        },
    })) == [
        ('1', 1.0),
        ('2', 1.0),
        ('3', 1.0),
        ('4', 1.0),
    ]

    assert get_hit_doc_id_and_score(es_master.search(index, body={
        'query': {
            'match_none': {},
        },
    })) == []

def test_query_match_operator(es_master, index):
    assert get_hit_doc_id_and_score(es_master.search(index, body={
        'query': {
            'match': {
                'title': {
                    'query': 'Shane Connelly',
                    'operator': 'or',   # default
                },
            },
        },
    })) == [
        ('3', 0.7985077),
        ('4', 0.662912),
        ('1', 0.13245322),
        ('2', 0.105360515),
    ]

    assert get_hit_doc_id_and_score(es_master.search(index, body={
        'query': {
            'match': {
                'title': {
                    'query': 'Shane Connelly',
                    'operator': 'and',
                },
            },
        },
    })) == [
        ('3', 0.7985077),
        ('4', 0.662912),
    ]

def test_query_match_analyzer(es_master, index):
    pass

def test_query_match_lenient(es_master, index):
    pass


# vi:et:ts=4:sw=4:cc=80
