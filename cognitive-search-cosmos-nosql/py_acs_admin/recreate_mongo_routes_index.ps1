# Delete and recreate the mongo-routes indexing.
#
# Note: delete in the sequence of indexer, index, datasource
# but recreate in the opposite sequence of datasource, index, indexer
#
# Chris Joakim, Microsoft

Write-Output 'deleting output tmp/ files ...'
del tmp\*.*

Write-Output '===================='
python search.py delete_indexer mongo-routes
sleep 5

Write-Output '===================='
python search.py delete_index mongo-routes
sleep 5

Write-Output '===================='
python search.py delete_datasource cosmosdb-mongo-dev-routes
sleep 30

Write-Output '===================='
python search.py create_cosmos_mongo_datasource dev routes
sleep 10

Write-Output '===================='
python search.py create_index mongo-routes mongo_routes_index
sleep 5

Write-Output '===================='
python search.py create_indexer mongo-routes mongo_routes_indexer
sleep 5

Write-Output '===================='
python search.py get_indexer_status mongo-routes
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
python search.py search_index mongo-routes route_clt_rdu
