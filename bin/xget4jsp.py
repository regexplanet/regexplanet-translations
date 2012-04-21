#!/usr/bin/python
#
# find translations that occur inside of html attributes (very common for .jsp's)
#

import optparse
import re
import sys

parser = optparse.OptionParser(usage="usage: %prog [options] jspfiles...")
parser.add_option("--quiet", action="store_false", default=True, dest="verbose", help="don't print status messages to stderr")

(options, args) = parser.parse_args()

if args == None or len(args) == 0:
	print("ERROR: you must specify at least one jsp file to search");
	sys.exit(1)

textPattern = re.compile("\"<%=_[hx]?\\(\"([^\"]+)\"\\)%>\"")

for srcfile in args:

	f = open(srcfile, 'r')

	for line in f:
		matcher = textPattern.search(line)

		while matcher:
			sys.stdout.write('_("%s")\n' % matcher.group(1))

			matcher = textPattern.search(line, matcher.end())

