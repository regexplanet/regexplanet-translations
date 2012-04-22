#!/bin/bash
#
# uses Google Translate to fill in untranslated entries in .po files
#

for f in ../text/??.po
do
	./gt4po.py --apikey=`cat /etc/fileformatnet/google-translate.key` --destlang=`basename $f .po` ../text/en.po
done

