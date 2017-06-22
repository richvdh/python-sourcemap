#!/usr/bin/env python
#
# decodes the sourcemap passed in on stdin
#
# eg: curl 'https://vector.im/beta/bundle.js.map' | ./decode.py
#
# outputs a series of:
#  <line #>:<col #>: <file>:<line #>:<col #> (name #)
#
# Includes vlq implementation from https://github.com/martine/python-sourcemap.

import json
import sys

import python_sourcemap

srcmap = json.load(sys.stdin)
line_table = python_sourcemap.decode_mappings(srcmap['mappings'])

for ln, line in enumerate(line_table):
    for cn in sorted(line.keys()):
        seg = line[cn]
        (src_id, src_line, src_col, name_id) = seg
        source = srcmap['sources'][src_id]
        print "%i:%i: '%s':%i:%i (%i)" % (ln+1, cn, source, src_line+1, src_col,
                                        name_id)
