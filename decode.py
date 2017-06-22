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

from __future__ import print_function

import codecs
import json
import sys

import python_sourcemap

# tell python it can write utf8 to stdout (even if it's piped somewhere else)
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

srcmap = json.load(sys.stdin)
line_table = python_sourcemap.decode_mappings(srcmap['mappings'])

for ln, line in enumerate(line_table):
    for cn in sorted(line.keys()):
        seg = line[cn]
        (src_id, src_line, src_col, name_id) = seg
        source = '<>'
        if src_id is not None:
            source = srcmap['sources'][src_id]
        name = '<>'
        if name_id is not None:
            name = srcmap['names'][name_id]
        print (
            "%i:%i: '%s':%i:%i (%s)" % (
                ln+1, cn, source, src_line+1, src_col, name,
            )
        )
