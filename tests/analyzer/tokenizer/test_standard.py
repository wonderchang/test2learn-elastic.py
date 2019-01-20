import pytest

from tests.analyzer.builder import IndexSettingBuilder


# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-tokenizer.html

@pytest.mark.parametrize('text,tokens', [
    ("What a wonderful world", ["What", "a", "wonderful", "world"]),
    ("Hi,\nCoffee or tea?\n", ["Hi", "Coffee", "or", "tea"]),
    ("Well-defined format", ["Well", "defined", "format"]),
    ("I'm so happy about that.", ["I'm", "so", "happy", "about", "that"]),
])
def test_standard(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "tokenizer": "standard",
        "text": text,
    }, tokens)


# vi:et:ts=4:sw=4:cc=80
