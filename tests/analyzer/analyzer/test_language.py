import uuid
import pytest

from tests.analyzer.builder import IndexSettingBuilder


@pytest.mark.parametrize('text,tokens', [
    ("activity", ["activ"]),
    ("lazy foxes", ["lazi", "fox"]),
    ("infos", ["info"]),
    ("He was disabled in the accident", ["he", "disabl", "accid"]),
])
def test_default(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "analyzer": "english",
        "text": text,
    }, tokens)


# vi:et:ts=4:sw=4:cc=80
