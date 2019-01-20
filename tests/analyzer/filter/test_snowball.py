import pytest

from tests.analyzer.builder import IndexSettingBuilder


# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-snowball-tokenfilter.html

@pytest.mark.parametrize('text,tokens', [
    ("What a wonderful world", ["What", "a", "wonder", "world"]),
    ("Hi, Coffee or tea?", ["Hi,", "Coffe", "or", "tea?"]),
])
def test_snowball(text, tokens, assert_token_analyze):
    # Default language is English
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": ["snowball"],
        "text": text,
    }, tokens)


# vi:et:ts=4:sw=4:cc=80
