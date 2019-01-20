import uuid
import pytest

from tests.analyzer.builder import IndexSettingBuilder


# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-whitespace-tokenizer.html

TOKENIZER = 'my-tokenizer'

@pytest.mark.parametrize('text,tokens', [
    ("What a wonderful world", ["What", "a", "wonderful", "world"]),
    ("Hi,\nCoffee or tea?\n", ["Hi,", "Coffee", "or", "tea?"]),
])
def test_whitespace(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "tokenizer": "whitespace",
        "text": text
    }, tokens)

@pytest.mark.parametrize('text,tokens', [
    ("What a wonderful world", ["What", "a", "wond", "erfu", "l", "worl", "d"]),
    ("Hi,\nCoffee or tea?\n", ["Hi,", "Coff", "ee", "or", "tea?"]),
])
def test_whitespace(text, tokens, assert_token_analyze):
    tokenizer = uuid.uuid4().hex
    settings = IndexSettingBuilder().tokenizer(tokenizer, {
        "type": "whitespace",
        "max_token_length": 4,
    }).build()
    assert_token_analyze({
        "tokenizer": tokenizer,
        "text": text
    }, tokens, settings)


# vi:et:ts=4:sw=4:cc=80
