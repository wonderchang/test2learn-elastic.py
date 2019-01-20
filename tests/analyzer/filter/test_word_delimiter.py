import uuid
import pytest

from tests.analyzer.builder import IndexSettingBuilder


# https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-word-delimiter-tokenfilter.html

@pytest.mark.parametrize('text,tokens', [
    ("PowerShot", ["Power", "Shot"]),
    ("ServerApi/CommonOptions", ["Server", "Api", "Common", "Options"]),
    ("common_options", ["common", "options"]),
    ("common-options", ["common", "options"]),
])
def test_default(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": ["word_delimiter"],
        "text": text,
    }, tokens)

@pytest.mark.parametrize('text,tokens', [
    ("502-42", ["502-42", "502", "42"]),
])
def test_preserve_original(text, tokens, assert_token_analyze):
    filter_ = uuid.uuid4().hex
    settings = IndexSettingBuilder().filter(filter_, {
        "type": "word_delimiter",
        "preserve_original": True,
    }).build()
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": [filter_],
        "text": text,
    }, tokens, settings)

@pytest.mark.parametrize('text,tokens', [
    ("wi-fi-512", ["wi", "wifi512", "fi", "512"]),
])
def test_catenate_all(text, tokens, assert_token_analyze):
    filter_ = uuid.uuid4().hex
    settings = IndexSettingBuilder().filter(filter_, {
        "type": "word_delimiter",
        "catenate_all": True
    }).build()
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": [filter_],
        "text": text,
    }, tokens, settings)

@pytest.mark.parametrize('text,tokens', [
    ("CommonOptions", ["CommonOptions", "Common", "Options"]),
    ("common_options", ["common_options", "common", "options"]),
])
def test_preserve_original(text, tokens, assert_token_analyze):
    filter_ = uuid.uuid4().hex
    settings = IndexSettingBuilder().filter(filter_, {
        "type": "word_delimiter",
        "preserve_original": True,
    }).build()
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": [filter_],
        "text": text,
    }, tokens, settings)

@pytest.mark.parametrize('text,tokens', [
    ("CommonOptions", ["CommonOptions", "Common", "Options"]),
    ("common_options", ["common_options", "common", "commonoptions", "options"]),
])
def test_preserve_original_catenate_all(text, tokens, assert_token_analyze):
    filter_ = uuid.uuid4().hex
    settings = IndexSettingBuilder().filter(filter_, {
        "type": "word_delimiter",
        "catenate_words": True,
        "preserve_original": True,
    }).build()
    assert_token_analyze({
        "tokenizer": "whitespace",
        "filter": [filter_, "unique"],
        "text": text,
    }, tokens, settings)


# vi:et:ts=4:sw=4:cc=80
