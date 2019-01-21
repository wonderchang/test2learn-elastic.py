import pytest


def test_multiple_templates_matching(es_master, create_index):
    common_analysis = {"analyzer": {"myanalyzer": {"type": "standard"}}}
    es_master.indices.put_template("common-analyzer", {
        "index_patterns": ["*"],
        "order": 0,
        "settings": {"analysis": common_analysis},
    })

    mappings1 = {"_source": {"enabled": False}}
    es_master.indices.put_template("private", {
        "index_patterns": ["private-*"],
        "order": 1,
        "mappings": {"_doc": mappings1},
    })

    mappings2 = {"properties": {"url": {"type": "text", "index": False}}}
    es_master.indices.put_template("public", {
        "index_patterns": ["public-*"],
        "order": 1,
        "mappings": {"_doc": mappings2},
    }, order=1)

    create_index("private-doc")
    create_index("public-doc")

    index1 = es_master.indices.get("private-doc")["private-doc"]
    assert index1["settings"]["index"]["analysis"] == common_analysis
    assert index1["mappings"]["_doc"] == mappings1

    index2 = es_master.indices.get("public-doc")["public-doc"]
    assert index2["settings"]["index"]["analysis"] == common_analysis
    assert index2["mappings"]["_doc"] == mappings2

    es_master.indices.delete_template("common-analyzer")
    es_master.indices.delete_template("public")
    es_master.indices.delete_template("private")


# vi:et:ts=4:sw=4:cc=80
