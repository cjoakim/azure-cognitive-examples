import os

from base import BaseClass

# An instance of this class is created in main class SearchClient.  It is used
# to generate all URL values used by this app to interact with Azure Cognitive Search.
#
# Chris Joakim, Microsoft

class Urls(BaseClass):

    def __init__(self):
        BaseClass.__init__(self)

    def list_indexes(self):
        return '{}/indexes?api-version={}'.format(self.search_url, self.search_api_version)

    def list_indexers(self):
        return '{}/indexers?api-version={}'.format(self.search_url, self.search_api_version)

    def list_datasources(self):
        return '{}/datasources?api-version={}'.format(self.search_url, self.search_api_version)

    def list_skillsets(self):
        return '{}/skillsets?api-version={}'.format(self.search_url, self.search_api_version)

    def get_index(self, name):
        return '{}/indexes/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def get_indexer(self, name):
        return '{}/indexers/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def get_indexer_status(self, name):
        return '{}/indexers/{}/status?api-version={}'.format(self.search_url, name, self.search_api_version)

    def get_datasource(self, name):
        return '{}/datasources/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def get_skillset(self, name):
        return '{}/skillsets/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def create_index(self):
        return '{}/indexes?api-version={}'.format(self.search_url, self.search_api_version)

    def modify_index(self, name):
        return '{}/indexes/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def create_indexer(self):
        return '{}/indexers?api-version={}'.format(self.search_url, self.search_api_version)

    def modify_indexer(self, name):
        return '{}/indexers/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def reset_indexer(self, name):
        return '{}/indexers/{}/reset?api-version={}'.format(self.search_url, name, self.search_api_version)

    def run_indexer(self, name):
        return '{}/indexers/{}/run?api-version={}'.format(self.search_url, name, self.search_api_version)

    def create_datasource(self):
        return '{}/datasources?api-version={}'.format(self.search_url, self.search_api_version)

    def modify_datasource(self, name):
        return '{}/datasources/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def create_synmap(self):
        return '{}/synonymmaps?api-version={}'.format(self.search_url, self.search_api_version)

    def modify_synmap(self, name):
        return '{}/synonymmaps/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def create_skillset(self):
        return '{}/skillsets?api-version={}'.format(self.search_url, self.search_api_version)

    def modify_skillset(self, name):
        return '{}/skillsets/{}?api-version={}'.format(self.search_url, name, self.search_api_version)

    def search_index(self, idx_name):
        return '{}/indexes/{}/docs/search?api-version={}'.format(self.search_url, idx_name, self.search_api_version)

    def lookup_doc(self, index_name, doc_key):
        return '{}/indexes/{}/docs/{}?api-version={}'.format(self.search_url, index_name, doc_key, self.search_api_version)



