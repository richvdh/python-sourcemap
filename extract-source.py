#!/usr/bin/env python3
#
# extracts a source file from the sourcemap passed in on stdin
#
# eg: curl 'https://vector.im/beta/bundle.js.map' | python-sourcemap/extract-source.py index.js

from __future__ import print_function

import json
import sys

source = sys.argv[1]

srcmap = json.load(sys.stdin)
source_table = srcmap['sources']

if source not in source_table:
    print ("%s not in source map" % source, file=sys.stderr)
    exit(1)
sourceidx = source_table.index(source)

print (srcmap['sourcesContent'][sourceidx])
