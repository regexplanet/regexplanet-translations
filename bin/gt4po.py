#!/usr/bin/python
#
# automated translation of a .PO file with the Google Ajax Lanague API
#
import json
import optparse
import os
import polib
import re
import requests
import sys
import time

parser = optparse.OptionParser(usage="usage: %prog [options] pofile...")
parser.add_option("--apikey", dest="apikey", help="Google Translate API key")
parser.add_option("--debug", action="store_true", default=False, dest="debug", help="print debugging messages to stdout")
parser.add_option("--destlang", dest="destlang", help="destination language(s), comma separated")
parser.add_option("--fuzzy", action="store_true", default=True, dest="fuzzy", help="flag translations as fuzzy (default)")
parser.add_option("--no-fuzzy", action="store_false", dest="fuzzy", help="do NOT flag translations as fuzzy")
parser.add_option("--sleep", default=0.10, dest="sleep", type='float', help="sleep interval between calls to Google Translate (in seconds)")
parser.add_option("--srclang", default="en", dest="srclang", help="source language (default=last 2 chars of base filename)")
parser.add_option("--quiet", action="store_false", default=True, dest="verbose", help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if args == None or len(args) == 0:
	print("ERROR: you must specify at least one po file to translate");
	sys.exit(1)

paramFix = re.compile("(\\(([0-9])\\))")

# deliberately primitive: snippets to translate can be very fragmented
html_re = re.compile("([^<]*<[^>]+>[^<]*)+")

for srcfile in args:

	if options.verbose:
		print("INFO: processing %s" % srcfile)

	if options.srclang == None:
		basename = os.path.splitext(srcfile)[0]
		options.srclang = basename[-2:]

	src_phrase = {}

	if options.verbose:
		print("INFO: reading %s..." % (srcfile))

	src_po = polib.pofile(srcfile, autodetect_encoding=False, encoding="utf-8", wrapwidth=-1)
	for entry in src_po:
		if entry.obsolete:
			continue

		#print("entry=%s: %s (%s, %s)" % (entry.msgid, entry.msgstr, entry.obsolete, entry.flags))

		src_phrase[entry.msgid] = entry.msgstr if len(entry.msgstr) > 0 else entry.msgid


	if options.verbose:
		print("INFO: %d phrases to translate from %s" % (len(src_phrase), options.srclang))

	destlangs = options.destlang.split(",")

	for destlang in destlangs:

		if destlang == options.srclang:
			if options.verbose:
				print("INFO: skipping %s (no need to translate self)" % destlang)
			continue

		dest_phrase = {}

		targetfile = os.path.splitext(srcfile)[0][:-2] + destlang + ".po"
		if os.path.exists(targetfile):
			if options.verbose:
				print("INFO: loading existing %s translations from %s" % (destlang, targetfile))
			dest_po = polib.pofile(targetfile, autodetect_encoding=False, encoding="utf-8", wrapwidth=-1)
			for entry in dest_po:

				if entry.obsolete or entry.msgstr == '':
					continue

				dest_phrase[entry.msgid] = entry.msgstr

			if options.verbose:
				print("INFO: %d existing translations loaded" % (len(dest_phrase)))
		else:
			# header needed so others will detect that it is UTF-8 encoded
			f = open(targetfile, 'wt')
			f.write('# created by GT4PO\n')
			f.write('msgid ""\n')
			f.write('msgstr ""\n');
			f.write('"Language: %s\\n"\n' % destlang);
			f.write('"MIME-Version: 1.0\\n"\n');
			f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n');
			f.write('"Content-Transfer-Encoding: 8bit\\n"\n');
			f.close()
			dest_po = polib.pofile(targetfile, autodetect_encoding=False, encoding="utf-8", wrapwidth=-1)


		if options.verbose:
			count = 0
			for key in src_phrase.keys():
				if key not in dest_phrase or len(dest_phrase[key]) == 0:
					count += 1
			print("INFO: %d phrases to translate from %s to %s" % (count, options.srclang, destlang))

		update_count = 0

		for key in src_phrase.keys():

			if key in dest_phrase and len(dest_phrase[key]) > 0:
				continue

			if options.sleep > 0:
				if options.debug:
					print("DEBUG: sleeping for %f" % options.sleep)
				time.sleep(options.sleep)

			headers = { 'User-Agent': 'gt4po.py', 'Referer': 'http://www.localeplanet.com/support/contact.html' }

			params = {}
			params['key'] = options.apikey
			params['q'] = src_phrase[key]
			params['source'] = options.srclang
			params['target'] = destlang
			params['format'] = 'html' if key.endswith('.html') else 'text'

			if options.debug:
				print('DEBUG: translating %s "%s"' % (params['format'], src_phrase[key]))

			r = requests.get(u"https://www.googleapis.com/language/translate/v2", params=params) #, headers=headers)

			if options.debug:
				print('DEBUG: Google Translate returns %d (%s)' % (r.status_code, r.content))

			if r.status_code != 200:
				print("ERROR: %d when translating %s (%s) to %s" % ( r.status_code, src_phrase[key], key, destlang))
				continue

			result = json.loads(r.content)

			text = result["data"]["translations"][0]["translatedText"]
			text = paramFix.sub("{\\2}", text)

			entry = dest_po.find(key)
			if entry:
				entry.msgstr = text
			else:
				entry = polib.POEntry(msgid=key, msgstr=text)
				dest_po.append(entry)

			update_count += 1

			if options.fuzzy:
				entry.flags.append("fuzzy")

		if options.verbose:
			print("INFO: saving %d changes to %s" % (update_count, targetfile))

		dest_po.save(targetfile)