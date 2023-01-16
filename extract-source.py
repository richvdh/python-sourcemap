#!/usr/bin/env python
#
# extracts a source file from the sourcemap passed in on stdin
#
# eg: curl 'https://vector.im/beta/bundle.js.map' | ./extract-source.py index.js
#
# omit source name to list sources

from __future__ import print_function

import json
import sys

def list_sources(srcmap):
    for k in srcmap['sources']:
        print(k)

def extract_source(srcmap, source):
    source_table = srcmap['sources']
    sourceidx = source_table.index(source)

    if sourceids < 0:
        print ("%s not in source map" % source, file=sys.stderr)
        exit(1)

    print (srcmap['sourcesContent'][sourceidx])


srcmap = json.load(sys.stdin)

if len(sys.argv) < 2:
    list_sources(srcmap)
else:
    extract_source(srcmap, sys.argv[1])
