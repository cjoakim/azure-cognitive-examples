#!/bin/bash

# Create the necessary tmp/ directories as they are git-ignored.
#
# Chris Joakim, Microsoft

mkdir -p py_acs_admin/tmp
mkdir -p java_acs_client/app/tmp
mkdir -p java_acs_client/tmp
mkdir -p py_cosmos_data/tmp

echo 'done'
