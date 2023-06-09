"""
Usage:
  python main.py <func> <args>
  python main.py wrangle_openflights_data
  python main.py wrangle_openflights_data | grep written
  -
  python main.py load_airport_data <db> <coll>
  python main.py load_airport_data dev airports
  -
  python main.py load_route_data <db> <coll>
  python main.py load_route_data dev routes
  -
  python main.py count_docs dev airports
  python main.py count_docs dev routes
  <
  python main.py truncate_container <db> <coll>
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
from pysrc.mongo import Mongo, MongoDBInstance, MongoDBDatabase, MongoDBCollection

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='0.1.0')
    print(arguments)

def wrangle_openflights_data():
    print('wrangle_openflights_data')
    parsed_airports, enhanced_routes = dict(), list()
    fake = Faker()

    lines = FS.read_lines('data/airports.json')
    for line in lines:
        try:
            airport = json.loads(line.strip())
            iata = airport['iata'].strip().upper()
            if len(iata) > 2:
                parsed_airport = parse_airport(airport)
                parsed_airport['pk'] = iata
                if parsed_airport != None:
                    parsed_airports[iata] = parsed_airport
                    if iata == 'CLT':
                        print(json.dumps(parsed_airport, sort_keys=False, indent=2))
        except:
            pass

    FS.write_json(parsed_airports, enhanced_airports_file())
    print('{} airports parsed'.format(len(parsed_airports)))
    airport_keys = parsed_airports.keys()

    lines = FS.read_lines('data/routes.json')
    for line_idx, line in enumerate(lines):
        try:
            route = json.loads(line.strip())
            source_iata = route['source_airport'].strip().upper()
            dest_iata = route['dest_airport'].strip().upper()
            if source_iata in airport_keys:
                if dest_iata in airport_keys:
                    route['pk'] = '{}:{}'.format(source_iata, dest_iata)
                    route['source_iata'] = source_iata
                    route['dest_iata']   = dest_iata
                    route['source_airport'] = parsed_airports[source_iata]
                    route['dest_airport'] = parsed_airports[dest_iata]
                    route['frequent_passengers'] = list()
                    if route['pk'] == 'CLT:RDU':
                        route['frequent_passengers'].append('Chris Joakim')
                    else:
                        for n in range(3):
                            route['frequent_passengers'].append(fake.name())
                    enhanced_routes.append(route)                 
                    if source_iata == 'CLT':
                        print(json.dumps(route, sort_keys=False, indent=2))
            else:
                print('line {} - route airport key(s) not found {} {}'.format(
                    line_idx, source_iata, dest_iata))
        except Exception as e:
            print(e)
    FS.write_json(enhanced_routes, enhanced_routes_file())
    print('{} enhanced_routes written'.format(len(enhanced_routes)))

def parse_airport(airport):
    try:
        airport['airport_id'] = int(airport['airport_id'])
        airport['latitude']  = float(airport['latitude'])
        airport['longitude'] = float(airport['longitude'])
        airport['altitude']  = float(airport['altitude'])
        airport['tz_offset'] = float(airport['tz_offset'])
        return airport
    except Exception as e:
        return None

def load_airport_data(dbname, cname):
    print('load_airport_data - dbname: {}, cname: {}'.format(dbname, cname))
    objects = FS.read_json(enhanced_airports_file())
    print('{} enhanced_airports loaded from file'.format(len(objects)))

    m = get_mongo_object(dbname, cname, False)

    for idx, key in enumerate(sorted(objects.keys())):
        if idx < 999999:
            print('---')
            obj = objects[key]
            obj['_id'] = str(uuid.uuid4())
            print(json.dumps(obj, sort_keys=False, indent=2))
            result = m.insert_doc(obj)
            print(result.inserted_id)

def load_route_data(dbname, cname):
    print('load_route_data - dbname: {}, cname: {}'.format(dbname, cname))
    objects = FS.read_json(enhanced_routes_file())
    print('{} enhanced_routes loaded from file'.format(len(objects)))

    m = get_mongo_object(dbname, cname, False)

    for idx, obj in enumerate(objects):
        if idx < 999999:
            print('---')
            obj['_id'] = str(uuid.uuid4())
            print(json.dumps(obj, sort_keys=False, indent=2))
            result = m.insert_doc(obj)
            print(result.inserted_id)

def count_docs(dbname, cname):
    print('count_docs - dbname: {}, cname: {}'.format(dbname, cname))

    m = get_mongo_object(dbname, cname, False)
    result = m.count_docs({})
    print('document count: {}'.format(result))

def truncate_container(dbname, cname):
    print('truncate_container - dbname: {}, cname: {}'.format(dbname, cname))

    m = get_mongo_object(dbname, cname, False)
    continue_to_processs, loop_counter = True, 0
    while continue_to_processs:
        loop_counter  = loop_counter + 1
        docs = m.find({}, 100)
        for doc in docs:
            m.delete_one(doc)
        count_result  = m.count_docs({})
        print('truncate_container - loop: {}, count: {}'.format(loop_counter, count_result))
        if count_result == 0:
            continue_to_processs = False
        if loop_counter > 999:
            continue_to_processs = False

def get_mongo_object(dbname, cname, verbose=False):
    opts = dict()
    opts['conn_string'] = get_conn_string()
    opts['verbose'] = False
    m = Mongo(opts)
    if dbname != None:
        m.set_db(dbname)
        if cname != None:
            m.set_coll(cname)
    return m

def get_conn_string():
    try:
        conn_string = Env.var('AZURE_COSMOSDB_MONGODB_CONN_STRING')
        if verbose():
            print("conn_string: {}".format(conn_string))
        return conn_string
    except Exception as e:
        print(e)
        return None

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
        if func == 'wrangle_openflights_data':
            wrangle_openflights_data()
        elif func == 'load_airport_data':
            dbname, cname = sys.argv[2], sys.argv[3]
            load_airport_data(dbname, cname)
        elif func == 'load_route_data':
            dbname, cname = sys.argv[2], sys.argv[3]
            load_route_data(dbname, cname)
        elif func == 'count_docs':
            dbname, cname = sys.argv[2], sys.argv[3]
            count_docs(dbname, cname)
        elif func == 'truncate_container':
            dbname, cname = sys.argv[2], sys.argv[3]
            truncate_container(dbname, cname)
        else:
            print_options('Error: invalid function: {}'.format(func))
