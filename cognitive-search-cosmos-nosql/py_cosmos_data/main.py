"""
Usage:
  python main.py <func> <args>
  -
  python main.py load_airport_data <db> <coll>
  python main.py load_airport_data dev airports
  -
  python main.py load_route_data <db> <coll>
  python main.py load_route_data dev routes
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# This is the entry-point for this Python application.
#
# Chris Joakim, Microsoft

import json
import sys
import uuid

from docopt import docopt
from faker import Faker

from pysrc.env import Env
from pysrc.fs import FS
from pysrc.cosmos import Cosmos


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='0.1.0')
    print(arguments)

def load_airport_data(dbname, cname):
    print('load_airport_data - dbname: {}, cname: {}'.format(dbname, cname))
    objects = FS.read_json(enhanced_airports_file())
    print('{} enhanced_airports loaded from file'.format(len(objects)))

    c = get_cosmos_object(dbname, cname, False)

    for idx, key in enumerate(sorted(objects.keys())):
        if idx < 999999:
            print('---')
            obj = objects[key]
            obj['id'] = str(uuid.uuid4())
            print(json.dumps(obj, sort_keys=False, indent=2))
            result = c.upsert_doc(obj)
            print(result)

def load_route_data(dbname, cname):
    print('load_route_data - dbname: {}, cname: {}'.format(dbname, cname))
    objects = FS.read_json(enhanced_routes_file())
    print('{} enhanced_routes loaded from file'.format(len(objects)))

    c = get_cosmos_object(dbname, cname, False)

    for idx, obj in enumerate(objects):
        if idx < 999999:
            print('---')
            obj['id'] = str(uuid.uuid4())
            print(json.dumps(obj, sort_keys=False, indent=2))
            result = c.upsert_doc(obj)
            print(result)

def get_cosmos_object(dbname, cname, verbose=False):
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_NOSQL_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_NOSQL_RW_KEY1')
    c = Cosmos(opts)
    if dbname != None:
        c.set_db(dbname)
        if cname != None:
            c.set_container(cname)
    return c

def enhanced_airports_file():
    return 'data/enhanced_airports.json'

def enhanced_routes_file():
    return 'data/enhanced_routes.json'

def verbose():
    for arg in sys.argv:
        if arg == '--verbose':
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options('Error: no command-line args')
    else:
        func = sys.argv[1].lower()
        if func == 'load_airport_data':
            dbname, cname = sys.argv[2], sys.argv[3]
            load_airport_data(dbname, cname)
        elif func == 'load_route_data':
            dbname, cname = sys.argv[2], sys.argv[3]
            load_route_data(dbname, cname)
        else:
            print_options('Error: invalid function: {}'.format(func))
