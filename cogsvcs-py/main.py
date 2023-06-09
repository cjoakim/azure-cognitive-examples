"""
Usage:
  python main.py <func> <args>
  python main.py text_translate_rest_supported_formats
  python main.py text_translate_rest

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

import requests

from docopt import docopt

from pysrc.env import Env
from pysrc.fs import FS

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version='0.1.0')
    print(arguments)


def text_translate_rest_supported_formats():
    url = get_target_url('translator/text/batch/v1.0/documents/formats')
    headers = get_rest_headers()

    print(url)
    print(headers)
    resp = requests.get(url, headers=headers)
    print(resp)
    FS.write_json(resp.json(), 'tmp/text_translate_rest_supported_formats.json')


def text_translate_rest():
    # https://learn.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/reference/rest-api-guide
    # https://learn.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/quickstarts/get-started-with-rest-api?pivots=programming-language-python
    # https://learn.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator-rest-api?tabs=csharp
    # gbbcjtexttran
    
    url = get_target_url('translator/text/batch/v1.0/batches')
    headers = get_rest_headers()

    print(url)
    print(headers)

def get_target_url(path):
    if get_rest_endpoint().endswith('/'):
        return '{}{}'.format(get_rest_endpoint(), path)
    else:
        return '{}/{}'.format(get_rest_endpoint(), path)

def get_rest_endpoint():
    return Env.var('AZURE_COGSVCS_ALLIN1_URL')

def get_rest_headers():
    key = Env.var('AZURE_COGSVCS_ALLIN1_KEY')
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json',
    }
    return headers


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
        if func == 'text_translate_rest_supported_formats':
            text_translate_rest_supported_formats()
        elif func == 'text_translate_rest':
            text_translate_rest()
        else:
            print_options('Error: invalid function: {}'.format(func))
