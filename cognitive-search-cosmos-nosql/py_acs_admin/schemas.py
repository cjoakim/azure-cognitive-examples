import json

from base import BaseClass

# An instance of this class is created in main class SearchClient.  It is used
# to read or generate and return the various JSON "schema" documents used in
# this app to interact with Azure Cognitive Search.
#
# Chris Joakim, Microsoft

class Schemas(BaseClass):
    """
    An instance of this class is created in main class SearchClient.  It is used
    to read or generate and return the various JSON "schema" documents used in
    this app to interact with Azure Cognitive Search.
    """

    def __init__(self):
        BaseClass.__init__(self)

    def blob_datasource_post_body(self):
        body = {
            "name" : "... populate me ...",
            "type" : "azureblob",
            "credentials" : {
                "connectionString" : "... populate me ..." },
                "container" :
                    { "name" : "... populate me ..." }
        }
        return body

    def cosmosdb_nosql_datasource_post_body(self):
        schema = {
            "name": "... populate me ...",
            "type": "cosmosdb",
            "credentials": {
                "connectionString": "... populate me ..."
            },
            "container": {
                "name": "... populate me ...",
                "query": None
            },
            "dataChangeDetectionPolicy": {
                "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
                "highWaterMarkColumnName": "_ts"
            }
        }
        return schema

    def cosmosdb_mongo_datasource_post_body(self):
        schema = {
            "name": "... populate me ...",
            "type": "cosmosdb",
            "credentials": {
                "connectionString": "... populate me ..."
            },
            "container": {
                "name": "... populate me ...",
                "query": None
            },
            "dataChangeDetectionPolicy": {
                "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
                "highWaterMarkColumnName": "_ts"
            },
            "dataDeletionDetectionPolicy": "null",
            "encryptionKey": "null",
            "identity": "null"
        }
        return schema
        # See https://learn.microsoft.com/en-us/azure/search/search-howto-index-cosmosdb-mongodb

    def sample_index_object(self, name):
        schema = {
            "name": name,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": "true", "searchable": "false", "filterable": "true"},
                {"name": "url", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "file_name", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "content", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "size", "type": "Edm.Int64", "searchable": "false", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "last_modified", "type": "Edm.DateTimeOffset", "searchable": "false", "filterable": "true", "sortable": "true", "facetable": "true"}
            ]
        }
        return schema

    def airports_index_schema(self, name):
        schema = {
            "name": name,
            "fields": [
                {"name": "pk", "type": "Edm.String", "key": "true", "filterable": "true"},
                {"name": "name", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "city", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "country", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "iata_code", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "latitude", "type": "Edm.Double", "searchable": "false", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "longitude", "type": "Edm.Double", "searchable": "false", "filterable": "true", "sortable": "true", "facetable": "true"},
                {"name": "timezone_code", "type": "Edm.String", "searchable": "true", "filterable": "true", "sortable": "true", "facetable": "true"}
            ]
        }
        return schema

    def indexer_schema(self, indexer_name, index_name, datasource_name):
        schema = {}
        schema['name'] = indexer_name
        schema['dataSourceName'] = datasource_name
        schema['targetIndexName'] = index_name
        schema['schedule'] = { "interval" : "PT2H" }
        return schema

    def sample_blob_indexer(self):
        # An indexer logically pairs a datasource to an index.
        # These metadata fields are available in Azure Blob Storage
        mappings = list()
        mappings.append({ "sourceFieldName" : "metadata_storage_size", "targetFieldName" : "size" })
        mappings.append({ "sourceFieldName" : "metadata_storage_path", "targetFieldName" : "url" })
        mappings.append({ "sourceFieldName" : "metadata_storage_last_modified", "targetFieldName" : "last_modified" })
        mappings.append({ "sourceFieldName" : "metadata_storage_name", "targetFieldName" : "file_name" })
        mappings.append({ "sourceFieldName" : "metadata_storage_path", "targetFieldName" : "id", "mappingFunction" : {"name" : "base64Encode" }})

        schema = {}
        schema['name'] = 'sample'
        schema['dataSourceName'] = 'azureblob-datasource'
        schema['targetIndexName'] = 'documents'
        schema['fieldMappings'] = mappings
        schema['schedule'] = { "interval" : "PT2H" }
        return schema

    def read(self, schema_base, values):
        schema_filename = 'schemas/{}.json'.format(schema_base)
        schema = self.load_json_file(schema_filename)
        for name in sorted(values.keys()):
            schema[name] = values[name]
        return schema

    def index_schema_diff(self, file1, file2):
        f1_schema = self.load_json_file(file1)
        f2_schema = self.load_json_file(file2)
        all_names, f1_dict, f2_dict, diffs = dict(), dict(), dict(), list()

        # gather the fields from both files
        for field in f1_schema['fields']:
            name = field['name']
            f1_dict[name] = field
            all_names[name] = name
        for field in f2_schema['fields']:
            name = field['name']
            f2_dict[name] = field
            all_names[name] = name

        # compare the entries in file1 vs file2
        for field_name in sorted(all_names.keys()):
            if (field_name in f1_dict.keys()) and (field_name in f2_dict.keys()):
                field1 = f1_dict[field_name]
                field2 = f2_dict[field_name]
                s1 = json.dumps(field1, sort_keys=True)
                s2 = json.dumps(field2, sort_keys=True)
                if s1 != s2:
                    diffs.append(('field is different', field_name, field1, field2))
            elif field_name in f1_dict.keys():
                field = f1_dict[field_name]
                diffs.append(('field not in file2', field_name, f1_dict[field_name]))
            elif field_name in f2_dict.keys():
                field = f2_dict[field_name]
                diffs.append(('field not in file1', field_name, f2_dict[field_name]))
        return diffs

    def indexer_schema_diff(self, file1, file2):
        f1_schema = self.load_json_file(file1)
        f2_schema = self.load_json_file(file2)
        all_names, f1_dict, f2_dict, diffs = dict(), dict(), dict(), list()

        # gather the fieldMappings fields from both files
        for field in f1_schema['fieldMappings']:
            name = field['sourceFieldName']
            f1_dict[name] = field
            all_names[name] = name
        for field in f2_schema['fieldMappings']:
            name = field['sourceFieldName']
            f2_dict[name] = field
            all_names[name] = name

        # gather the outputFieldMappings fields from both files
        for field in f1_schema['outputFieldMappings']:
            name = field['sourceFieldName']
            f1_dict[name] = field
            all_names[name] = name
        for field in f2_schema['outputFieldMappings']:
            name = field['sourceFieldName']
            f2_dict[name] = field
            all_names[name] = name

        # compare the entries in file1 vs file2
        for field_name in sorted(all_names.keys()):
            if (field_name in f1_dict.keys()) and (field_name in f2_dict.keys()):
                field1 = f1_dict[field_name]
                field2 = f2_dict[field_name]
                s1 = json.dumps(field1, sort_keys=True)
                s2 = json.dumps(field2, sort_keys=True)
                if s1 != s2:
                    diffs.append(('field is different', field_name, field1, field2))
            elif field_name in f1_dict.keys():
                field = f1_dict[field_name]
                diffs.append(('field not in file2', field_name, f1_dict[field_name]))
            elif field_name in f2_dict.keys():
                field = f2_dict[field_name]
                diffs.append(('field not in file1', field_name, f2_dict[field_name]))
        return diffs
