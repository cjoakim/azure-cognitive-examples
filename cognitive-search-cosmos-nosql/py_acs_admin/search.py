"""
Usage:
    python search.py display_env
    -
    python search.py create_cosmos_mongo_datasource <db> <collection>
    python search.py create_cosmos_mongo_datasource dev airports --no-http
    python search.py create_cosmos_mongo_datasource dev airports
    python search.py create_cosmos_mongo_datasource dev routes
    -
    python search.py create_cosmos_nosql_datasource dev airports
    -
    python search.py delete_datasource <name>
    python search.py delete_datasource cosmosdb-nosql-dev-airports
    -
    python search.py list_indexes
    python search.py list_indexers
    python search.py list_datasources
    -
    python search.py get_xxx <name>
    python search.py get_index mongo-airports
    python search.py get_index mongo-routes
    python search.py get_indexer mongo-airports
    python search.py get_indexer mongo-routes
    python search.py get_indexer_status mongo-airports
    python search.py get_indexer_status mongo-routes
    python search.py get_datasource cosmosdb-mongo-dev-airports
    python search.py get_datasource cosmosdb-mongo-dev-routes
    -
    python search.py create_index <index_name> <schema_file>
    python search.py create_index mongo-airports mongo_airports_index
    python search.py create_index mongo-routes mongo_routes_index
    python search.py delete_index mongo-airports
    -
    python search.py create_indexer mongo-airports mongo_airports_indexer
    python search.py create_indexer mongo-routes mongo_routes_indexer
    python search.py delete_indexer mongo-airports
    python search.py run_indexer mongo-airports
    -
    python search.py create_synmap airports synonym_map_airports
    python search.py update_synmap airports synonym_map_airports
    python search.py delete_synmap airports 
    -
    python search.py search_index mongo-airports all_airports
    python search.py search_index mongo-airports airports_charl
    python search.py search_index mongo-airports airports_clt
    python search.py search_index mongo-airports airports_campy
    python search.py search_index mongo-airports airports_lucene_east_cl_south 
    -
    python search.py search_index mongo-routes route_clt_rdu
    -
    python search.py lookup_doc mongo-airports eVBWc0FPdExvZzJYQXdBQUFBQUFBQT090
"""

import json
import os
import sys
import time
import traceback

import requests

from docopt import docopt

from base import BaseClass
from schemas import Schemas
from urls import Urls

# This is the main class in this subject, and the command-line entry point.
# It is used to invoke the Azure Cognitive Search HTTP endpoint via the REST
# API.  The Python requests library is used for all HTTP functionality.
#
# Chris Joakim, Microsoft

class SearchClient(BaseClass):

    def __init__(self):
        BaseClass.__init__(self)
        self.u = None  # the current url
        self.r = None  # the current requests response object
        self.config = dict()
        self.schemas = Schemas()
        self.urls = Urls()

        self.named_searches = self.named_searches_dict()

        self.admin_headers = dict()
        self.admin_headers['Content-Type'] = 'application/json'
        self.admin_headers['api-key'] = self.search_admin_key

        self.query_headers = dict()
        self.query_headers['Content-Type'] = 'application/json'
        self.query_headers['api-key'] = self.search_query_key

    def display_env(self):
        print('search_name:      {}'.format(self.search_name))
        print('search_url:       {}'.format(self.search_url))
        print('search_admin_key: {}'.format(self.search_admin_key))
        print('search_query_key: {}'.format(self.search_query_key))
        print('admin_headers:\n{}'.format(json.dumps(self.admin_headers, sort_keys=False, indent=2)))
        print('query_headers:\n{}'.format(json.dumps(self.query_headers, sort_keys=False, indent=2)))

    def list_indexes(self):
        url = self.urls.list_indexes()
        self.http_request('list_indexes', 'get', url, self.admin_headers)

    def list_indexers(self):
        url = self.urls.list_indexers()
        self.http_request('list_indexers', 'get', url, self.admin_headers)

    def list_datasources(self):
        url = self.urls.list_datasources()
        self.http_request('list_datasources', 'get', url, self.admin_headers)

    def get_index(self, name):
        url = self.urls.get_index(name)
        self.http_request('get_index', 'get', url, self.admin_headers)

    def get_indexer(self, name):
        url = self.urls.get_indexer(name)
        self.http_request('get_indexer', 'get', url, self.admin_headers)

    def get_indexer_status(self, name):
        url = self.urls.get_indexer_status(name)
        self.http_request('get_indexer_status', 'get', url, self.admin_headers)

    def get_datasource(self, name):
        url = self.urls.get_datasource(name)
        self.http_request('get_datasource', 'get', url, self.admin_headers)

    def create_index(self, name, schema_file):
        self.modify_index('create', name, schema_file)

    def update_index(self, name, schema_file):
        self.modify_index('update', name, schema_file)

    def delete_index(self, name):
        self.modify_index('delete', name, None)

    def modify_index(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema = self.schemas.read(schema_file, {'name': name})

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_index()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_index(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_index(name)

        function = '{}_index_{}'.format(action, name)
        self.http_request(function, http_method, url, self.admin_headers, schema)

    def create_indexer(self, name, schema_file):
        self.modify_indexer('create', name, schema_file)

    def update_indexer(self, name, schema_file):
        self.modify_indexer('update', name, schema_file)

    def delete_indexer(self, name):
        self.modify_indexer('delete', name, None)

    def modify_indexer(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema = self.schemas.read(schema_file, {'name': name})

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_indexer()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_indexer(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_indexer(name)

        function = '{}_indexer_{}'.format(action, name)
        self.http_request(function, http_method, url, self.admin_headers, schema)

    def reset_indexer(self, name):
        url = self.urls.reset_indexer(name)
        self.http_request('reset_indexer', 'post', url, self.admin_headers)

    def run_indexer(self, name):
        url = self.urls.run_indexer(name)
        self.http_request('run_indexer', 'post', url, self.admin_headers)

    def create_cosmos_nosql_datasource(self, dbname, container):
        conn_str = self.cosmos_nosql_datasource_name_conn_str(dbname)
        body = self.schemas.cosmosdb_nosql_datasource_post_body()
        body['name'] = self.cosmos_nosql_datasource_name(dbname, container)
        body['credentials']['connectionString'] = conn_str
        body['container']['name'] = container
        print(json.dumps(body, sort_keys=False, indent=2))

        url = self.urls.create_datasource()
        function = 'create_cosmos_nosql_datasource_{}_{}'.format(dbname, container)
        self.http_request(function, 'post', url, self.admin_headers, body)

    def create_cosmos_mongo_datasource(self, dbname, container):
        conn_str = self.cosmos_mongo_datasource_name_conn_str(dbname)
        body = self.schemas.cosmosdb_mongo_datasource_post_body()
        body['name'] = self.cosmos_mongo_datasource_name(dbname, container)
        body['credentials']['connectionString'] = conn_str
        body['container']['name'] = container
        body['dataDeletionDetectionPolicy'] = None
        body['encryptionKey'] = None
        body['identity'] = None

        url = self.urls.create_datasource()
        function = 'create_cosmos_mongo_datasource_{}_{}'.format(dbname, container)
        self.http_request(function, 'post', url, self.admin_headers, body)

    def delete_datasource(self, name):
        url = self.urls.modify_datasource(name)
        function = 'delete_datasource{}'.format(name)
        self.http_request(function, 'delete', url, self.admin_headers, None)

    def create_synmap(self, name, schema_file):
        self.modify_synmap('create', name, schema_file)

    def update_synmap(self, name, schema_file):
        self.modify_synmap('update', name, schema_file)

    def delete_synmap(self, name):
        self.modify_synmap('delete', name, None)

    def modify_synmap(self, action, name, schema_file):
        # read the schema json file if necessary
        schema = None
        if action in ['create', 'update']:
            schema_file = 'schemas/{}.json'.format(schema_file)
            schema = self.load_json_file(schema_file)
            schema['name'] = name

        if action == 'create':
            http_method = 'post'
            url = self.urls.create_synmap()
        elif action == 'update':
            http_method = 'put'
            url = self.urls.modify_synmap(name)
        elif action == 'delete':
            http_method = 'delete'
            url = self.urls.modify_synmap(name)

        function = '{}_synmap_{}'.format(action, name)
        self.http_request(function, http_method, url, self.admin_headers, schema)

    def search_index(self, idx_name, search_name, additional):
        print('---')
        print('search_index: {} -> {} | {}'.format(idx_name, search_name, additional))
        url = self.urls.search_index(idx_name)
        print('search_index url: {}'.format(url))

        if search_name in self.named_searches.keys(): 
            search_params = self.named_searches[search_name]
            print('named_search found: {}  params: {}'.format(search_name, search_params))
        else:
            search_params = self.named_searches['all_airports']
            print('named_search not found: {}  using default params: {}'.format(search_name, search_params)) 

        print('url:     {}'.format(url))
        print('method:  {}'.format('POST'))
        print('params:  {}'.format(search_params))
        print('headers: {}'.format(self.admin_headers))

        r = requests.post(url=url, headers=self.admin_headers, json=search_params)
        print('response: {}'.format(r))
        if r.status_code == 200:
            resp_obj = json.loads(r.text)
            print(json.dumps(resp_obj, sort_keys=False, indent=2))
            print('response document count: {}'.format(resp_obj['@odata.count']))
            outfile = 'tmp/search_{}.json'.format(search_name)
            self.write_json_file(resp_obj, outfile)

    def named_searches_dict(self):
        if False:
            searches = dict()
            searches['all_airports'] = {'count': True, 'search': '*', 'orderby': 'pk'}
            searches['all_airports_charl'] = {'count': True, 'search': 'charl*', 'orderby': 'pk', 'select': 'name,city,pk'}
            searches['all_airports_charl_lucene'] = {'count': True, 'search': 'charl*', 'orderby': 'pk', 'select': 'name,city,pk', 'queryType': 'full'}
            searches['all_documents'] = {'count': True, 'search': '*', 'orderby': 'id'}
            searches['top_words_'] = {'count': True, 'search': '*', 'orderby': 'id'}
            self.write_json_file(searches, 'searches_generated.json')
        else:
            searches = self.load_json_file('searches.json')
        return searches

    def lookup_doc(self, index_name, doc_key):
        print('lookup_doc: {} {}'.format(index_name, doc_key))
        # See https://docs.microsoft.com/en-us/rest/api/searchservice/lookup-document#examples
        # GET /indexes/hotels/docs/2?api-version=2020-06-30
        url = self.urls.lookup_doc(index_name, doc_key)
        headers = self.query_headers
        print(url)
        print(headers)
        function = 'lookup_doc_{}_{}'.format(index_name, doc_key)
        r = self.http_request(function, 'get', url, self.query_headers)

    def http_request(self, function_name, method, url, headers={}, json_body={}):
        # This is a generic method which invokes ALL HTTP Requests to the Azure Search Service
        print('===')
        print("http_request: {} {} {}\nheaders: {}\nbody: {}".format(
            function_name, method.upper(), url, headers, json_body))

        print("http_request name/method/url: {} {} {}".format(
            function_name, method.upper(), url))
        print("http_request headers:\n{}".format(json.dumps(
            headers, sort_keys=False, indent=2)))
        print("http_request body:\n{}".format(json.dumps(
            json_body, sort_keys=False, indent=2)))

        if self.no_http():
            print('http_request bypassed per command-line arg')
            return {}
        else:
            print('---')
            r = None
            if method == 'get':
                r = requests.get(url=url, headers=headers)
            elif method == 'post':
                r = requests.post(url=url, headers=headers, json=json_body)
            elif method == 'put':
                r = requests.put(url=url, headers=headers, json=json_body)
            elif method == 'delete':
                r = requests.delete(url=url, headers=headers)
            else:
                print('error; unexpected method value passed to invoke: {}'.format(method))

            print('response: {}'.format(r))
            if r.status_code < 300:
                try:
                    # Save the request and response data as a json file in tmp/
                    outfile  = 'tmp/{}_{}.json'.format(function_name, int(self.epoch()))
                    data = dict()
                    data['function_name'] = function_name
                    data['method'] = method
                    data['url'] = url
                    data['body'] = json_body
                    data['filename'] = outfile
                    data['resp_status_code'] = r.status_code
                    try:
                        data['resp_obj'] = r.json()
                    except:
                        pass # this is expected as some requests don't return a response, like http 204
                    self.write_json_file(data, outfile)
                except Exception as e:
                    print("exception saving http response".format(e))
                    print(traceback.format_exc())
            else:
                print(r.text)
            return r

    def epoch(self):
        return time.time()
    
    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def no_http(self):
        for arg in sys.argv:
            if arg == '--no-http':
                return True
        return False


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        print('func: {}'.format(func))
        client = SearchClient()

        if func == 'display_env':
            client.display_env()

        elif func == 'list_indexes':
            client.list_indexes()

        elif func == 'list_indexers':
            client.list_indexers()

        elif func == 'list_datasources':
            client.list_datasources()

        elif func == 'get_index':
            name = sys.argv[2]
            client.get_index(name)

        elif func == 'get_indexer':
            name = sys.argv[2]
            client.get_indexer(name)

        elif func == 'get_indexer_status':
            name = sys.argv[2]
            client.get_indexer_status(name)

        elif func == 'get_datasource':
            name = sys.argv[2]
            client.get_datasource(name)

        elif func == 'create_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_index(index_name, schema_file)

        elif func == 'update_index':
            index_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_index(index_name, schema_file)

        elif func == 'delete_index':
            name = sys.argv[2]
            client.delete_index(name)

        elif func == 'create_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_indexer(indexer_name, schema_file)

        elif func == 'update_indexer':
            indexer_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_indexer(indexer_name, schema_file)

        elif func == 'delete_indexer':
            name = sys.argv[2]
            client.delete_indexer(name)

        elif func == 'reset_indexer':
            name = sys.argv[2]
            client.reset_indexer(name)

        elif func == 'run_indexer':
            name = sys.argv[2]
            client.run_indexer(name)

        elif func == 'create_cosmos_nosql_datasource':
            dbname = sys.argv[2]
            container = sys.argv[3]
            client.create_cosmos_nosql_datasource(dbname, container)

        elif func == 'create_cosmos_mongo_datasource':
            dbname = sys.argv[2]
            container = sys.argv[3]
            client.create_cosmos_mongo_datasource(dbname, container)

        elif func == 'delete_datasource':
            name = sys.argv[2]
            client.delete_datasource(name)

        elif func == 'create_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.create_synmap(synmap_name, schema_file)

        elif func == 'update_synmap':
            synmap_name = sys.argv[2]
            schema_file = sys.argv[3]
            client.update_synmap(synmap_name, schema_file)

        elif func == 'delete_synmap':
            synmap_name = sys.argv[2]
            client.delete_synmap(synmap_name)

        elif func == 'search_index':
            index_name  = sys.argv[2]
            search_name = sys.argv[3]
            additional  = None
            if len(sys.argv) > 4:
                additional = sys.argv[4]
            client.search_index(index_name, search_name, additional)

        elif func == 'lookup_doc':
            index_name  = sys.argv[2]
            doc_key     = sys.argv[3]
            client.lookup_doc(index_name, doc_key)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
