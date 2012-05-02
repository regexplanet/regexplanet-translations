#!/bin/bash
#
# processes .po files to be digestible by RegexPlanet java
#

for f in ../text/??.po
do
	./po2prop.py $f
	mv ../text/`basename $f .po`.properties ../../rxp/src/com/regexplanet/i18n/text/
done


