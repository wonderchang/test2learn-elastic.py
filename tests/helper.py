

def get_hit_doc_id_and_score(results):
    return [(hit['_id'], hit['_score']) for hit in results['hits']['hits']]



# vi:et:ts=4:sw=4:cc=80
