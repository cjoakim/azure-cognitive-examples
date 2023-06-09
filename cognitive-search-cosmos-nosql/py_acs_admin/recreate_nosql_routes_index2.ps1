# Delete and recreate the nosql-routes2 indexing.
#
# Note: delete in the sequence of indexer, index, datasource
# but recreate in the opposite sequence of datasource, index, indexer
#
# Chris Joakim, Microsoft

Write-Output 'deleting output tmp/ files ...'
del tmp\*.*

Write-Output '===================='
python search.py delete_indexer nosql-routes2
sleep 5

Write-Output '===================='
python search.py delete_index nosql-routes2
sleep 5

Write-Output '===================='
python search.py delete_datasource cosmosdb-nosql-search-routes2
sleep 30

Write-Output '===================='
python search.py create_cosmos_nosql_datasource search routes
sleep 10

Write-Output '===================='
python search.py create_index nosql-routes2 nosql_routes_index
sleep 5

Write-Output '===================='
python search.py create_indexer nosql-routes2 nosql_routes_indexer
sleep 5

Write-Output '===================='
python search.py get_indexer_status nosql-routes2
sleep 5

Write-Output '===================='
python search.py update_synmap routes synonym_map_routes
sleep 5

Write-Output '===================='
python search.py list_datasources
sleep 5

Write-Output '===================='
python search.py list_indexes
sleep 5

Write-Output '===================='
python search.py list_indexers
sleep 5

Write-Output 'pausing to let the indexer run ...'
sleep 60

Write-Output '===================='
python search.py search_index nosql-routes2 route_clt_rdu
