from time import sleep


def test_shard_primary_replica_allocation(es_master, create_index):
    index = create_index(body={
        'settings': {
            'number_of_shards': 2,
            'number_of_replicas': 1,
        }
    })

    body = {
        'title': 'Hi',
        'content': 'No more',
    }
    es_master.index(index, 'doc', body, 1, refresh=True)

    results = es_master.cat.shards(index, format='json')

    assert len(results) == 4

    assert results[0]['shard'] == '1'
    assert results[0]['prirep'] == 'r'  # replica
    assert results[1]['shard'] == '1'
    assert results[1]['prirep'] == 'p'  # primary
    assert results[0]['node'] != results[1]['node']

    assert results[2]['shard'] == '0'
    assert results[2]['prirep'] == 'p'  # primary
    assert results[3]['shard'] == '0'
    assert results[3]['prirep'] == 'r'  # replica
    assert results[2]['node'] != results[3]['node']

    # node 1 (shard-0-primary, shard-1-replica)
    # node 2 (shard-0-replica, shard-1-primary)
    assert results[0]['node'] == results[2]['node']
    assert results[1]['node'] == results[3]['node']


# vi:et:ts=4:sw=4:cc=80
