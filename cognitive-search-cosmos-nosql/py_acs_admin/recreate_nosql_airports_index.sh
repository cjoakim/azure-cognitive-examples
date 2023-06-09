#!/bin/bash

# Delete and recreate the nosql-airports indexing.
#
# Note: delete in the sequence of indexer, index, datasource
# but recreate in the opposite sequence of datasource, index, indexer
#
# Chris Joakim, Microsoft

echo 'deleting output tmp/ files ...'
del tmp/*.*

echo '===================='
python search.py delete_indexer nosql-airports
sleep 5

echo '===================='
python search.py delete_index nosql-airports
sleep 5

echo '===================='
python search.py delete_datasource cosmosdb-nosql-dev-airports
sleep 30

echo '===================='
python search.py create_cosmos_nosql_datasource dev airports
sleep 10

echo '===================='
python search.py create_index nosql-airports nosql_airports_index
sleep 5

echo '===================='
python search.py create_indexer nosql-airports nosql_airports_indexer
sleep 5

echo '===================='
python search.py get_indexer_status nosql-airports
sleep 5

echo '===================='
python search.py update_synmap airports synonym_map_airports
sleep 5

echo '===================='
python search.py list_datasources
sleep 5

echo '===================='
python search.py list_indexes
sleep 5

echo '===================='
python search.py list_indexers
sleep 5

echo 'pausing to let the indexer run ...'
sleep 60

echo '===================='
python search.py search_index nosql-airports airports_clt
