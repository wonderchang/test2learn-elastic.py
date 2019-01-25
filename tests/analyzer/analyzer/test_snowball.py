import uuid
import pytest

from tests.analyzer.builder import IndexSettingBuilder


@pytest.mark.parametrize('text,tokens', [
    ("infos", ["info"]),
    ("oranges", ["orang"]),
    ("useful", ["use"]),
    ("disable", ["disabl"]),
    ("alias", ["alia"]),
    ("activity", ["activ"]),
])
def test_default(text, tokens, assert_token_analyze):
    analyzer = uuid.uuid4().hex
    settings = IndexSettingBuilder().analyzer(analyzer, {
        "type": "snowball",
    }).build()
    assert_token_analyze({
        "analyzer": analyzer,
        "text": text,
    }, tokens, settings)


# vi:et:ts=4:sw=4:cc=80
