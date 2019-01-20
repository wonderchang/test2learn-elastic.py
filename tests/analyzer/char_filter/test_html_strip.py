import pytest


@pytest.mark.parametrize('text,tokens', [
    ("<p>I&apos;m so <b>happy</b>!</p>", ["\nI'm so happy!\n"]),
])
def test_filter_html_strip(text, tokens, assert_token_analyze):
    assert_token_analyze({
        "tokenizer": "keyword",
        "char_filter": ["html_strip"],
        "text": text
    }, tokens)


# vi:et:ts=4:sw=4:cc=80
