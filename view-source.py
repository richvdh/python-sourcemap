#!/usr/bin/env python
#
# view the source corresponding to a line in a sourcemap
#
# eg: curl 'https://vector.im/beta/bundle.js.map' | ./view-source.py 27:31742

from __future__ import print_function

import json
import StringIO
import subprocess
import sys

import python_sourcemap

parts = sys.argv[1].split(':', 1)
(line, col) = (int(parts[0]), 0)
if len(parts) > 1:
    col = int(parts[1])

srcmap = json.load(sys.stdin)
line_table = python_sourcemap.decode_mappings(srcmap['mappings'])

if line >= len(line_table):
    print ("%i beyond end of source map" % line, file=sys.stderr)
    exit(1)

entry = line_table[line-1]

# find the last entry whose col is before the desired col.
found_col = None
for k in sorted(entry.keys()):
    if found_col is None:
        found_col = k
    # k is zero-based, col is 1-based, so >=
    if k >= col:
        break
    found_col = k

if found_col is None:
    print ("No source map entries for %i" % line, file=sys.stderr)
    exit(1)

(src_id, src_line, src_col, name_id) = entry[found_col]
# fix zero offsets
src_line += 1
src_col += 1
source_name = srcmap['sources'][src_id]
print ("source: %s, line: %i, col: %i" % (source_name, src_line, src_col))

# pipe the source into 'less'
proc = subprocess.Popen("less +%i" % src_line, shell=True, stdin=subprocess.PIPE)
proc.communicate(input=srcmap['sourcesContent'][src_id])
exit (proc.returncode)
