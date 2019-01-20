# Test2learn Elasticsearch

Prerequisite:

  * make 3.81
  * Docker 18.09.1

Build minimal learnable Elasticsearch clusters

    make

Wait for container health checks

    $ docker ps --format "table {{.Names}}\t{{.Status}}"
    NAMES               STATUS
    es-master-n1        Up 4 minutes (healthy)
    es-master-n2        Up 4 minutes (healthy)
    es-replica-n1       Up 4 minutes (healthy)
    es-replica-n2       Up 4 minutes (healthy)

Run tests to learn

    make test

## Minimal learnable architecture

```
             Docker Guest              |         Host
                                       |
                                       |
 master --*--- es-master-n1:9200 <-----|-----> localhost:9200
          |                            |
          *--- es-master-n2:9200 <-----|-----> localhost:9201
                                       |
replica --*-- es-replica-n1:9200 <-----|-----> localhost:9210
          |                            |
          *-- es-replica-n2:9200 <-----|-----> localhost:9211
                                       |
                                       |
 ------- (network: es-network) ------- |
                  ^                    |
                  |                    |
                  v                    |
            test2learn-es <------------|----- $ make test
  (pytest, elasticsearch-py-client)    |
                                       |
```


<!--
  vi:wrap:et:ts=2:sw=2
--> 
