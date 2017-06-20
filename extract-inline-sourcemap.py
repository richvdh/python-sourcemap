#!/usr/bin/env python
#
# extract an inline source map from the file passed in on stdin

from __future__ import print_function

import base64
import re
import sys

c = re.compile('^//# sourceMappingURL=');
url = None

for line in sys.stdin:
    match = c.match(line);
    if not match:
        continue
    if url:
        print("multiple sourceMappingURLs", file=sys.stderr)
    url = line[match.end():].strip()

if not url:
    print("no sourceMappingURL in file", file=sys.stderr)
    sys.exit(1)

(scheme, rest) = url.split(':', 1)
if scheme != 'data':
    print("not an inline sourcemap: %s" % (url), file=sys.stderr)
    sys.exit(1)

(mime_type,data) = rest.split(',', 1)
if mime_type != 'application/json;charset=utf-8;base64':
    print("unexpected mime-type: %s" % mime_type, file=sys.stderr)
    sys.exit(1)

print(base64.b64decode(data))
