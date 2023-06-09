import json
import os
import sys
import time

# This is the abstract superclass of the several classes in this project -
# SearchClient, Schemas, Urls.
#
# Chris Joakim, Microsoft

class BaseClass:

    def __init__(self):
        self.user_agent = {'User-agent': 'Mozilla/5.0'}
        self.search_name = os.environ['AZURE_SEARCH_NAME']
        self.search_url  = os.environ['AZURE_SEARCH_URL']
        self.search_admin_key = os.environ['AZURE_SEARCH_ADMIN_KEY']
        self.search_query_key = os.environ['AZURE_SEARCH_QUERY_KEY']
        self.search_api_version = '2021-04-30-Preview'

        if self.search_url.endswith('/'):
            self.search_url = self.search_url[:-1]

    def epoch(self):
        return time.time()

    def blob_datasource_name(self, container):
        return 'azureblob-{}'.format(container)

    def cosmos_nosql_datasource_name(self, dbname, container):
        return 'cosmosdb-nosql-{}-{}'.format(dbname, container)

    def cosmos_mongo_datasource_name(self, dbname, container):
        return 'cosmosdb-mongo-{}-{}'.format(dbname, container)

    def cosmos_mongo_datasource_name_conn_str(self, dbname):
        # See https://learn.microsoft.com/en-us/azure/search/search-howto-index-cosmosdb-mongodb
        # "connectionString": "AccountEndpoint=https://[cosmos-account-name].documents.azure.com;AccountKey=[cosmos-account-key];Database=[cosmos-database-name];ApiKind=MongoDb;"
        acct = os.environ['AZURE_COSMOSDB_MONGODB_USER']
        key  = os.environ['AZURE_COSMOSDB_MONGODB_PASS']
        return 'AccountEndpoint=https://{}.documents.azure.com;AccountKey={};Database={};ApiKind=MongoDb;'.format(
            acct, key, dbname)

    def read_text_file(self, infile):
        lines = list()
        with open(infile, 'rt') as f:
            for idx, line in enumerate(f):
                lines.append(line.strip())
        return lines

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))
