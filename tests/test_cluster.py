

def test_health(es_master, es_replica):
    master = es_master.cluster.health()
    assert master['cluster_name'] == 'es-master'
    assert master['status'] == 'green'
    assert master['number_of_nodes'] == 2

    replica = es_replica.cluster.health()
    assert replica['cluster_name'] == 'es-replica'
    assert replica['status'] == 'green'
    assert replica['number_of_nodes'] == 2


# vi:et:ts=4:sw=4:cc=80
