import pytest

from tests.analyzer.builder import IndexSettingBuilder


# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-letter-tokenizer.html

@pytest.mark.parametrize('text,tokens', [
    ("The 4th floor roomer", ["The", "th", "floor", "roomer"]),
])
def test_standard(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "tokenizer": "letter",
        "text": text,
    }, tokens)


# vi:et:ts=4:sw=4:cc=80
