

class IndexSettingBuilder:

    def __init__(self):
        self._char_filter = {}
        self._tokenizer = {}
        self._filter = {}
        self._analyzer = {}

    def char_filter(self, name, setting):
        self._char_filter[name] = setting
        return self

    def tokenizer(self, name, setting):
        self._tokenizer[name] = setting
        return self

    def filter(self, name, setting):
        self._filter[name] = setting
        return self

    def analyzer(self, name, setting):
        self._analyzer[name] = setting
        return self

    def build(self):
        return {
            "settings": {
                "analysis": {
                    "char_filter": self._char_filter,
                    "tokenizer": self._tokenizer,
                    "filter": self._filter,
                    "analyzer": self._analyzer,
                }
            }
        }


# vi:et:ts=4:sw=4:cc=80
