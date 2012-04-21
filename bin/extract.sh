#!/bin/bash
#
# extract translatable strings
#


find ../../rxp/src -name "*.java" >files.tmp
find ../../rxp/www -name "*.jsp" >>files.tmp
find ../../rxp/www -name "*.inc" >>files.tmp

find ../../rxp/www -name "*.jsp" | xargs ./xget4jsp.py >xgetjsp.tmp
echo "./xgetjsp.tmp" >>files.tmp

xgettext \
	--files-from=files.tmp \
	--foreign-user \
	--from-code=UTF-8 \
	--keyword \
	--keyword=_ \
	--keyword=_h \
	--keyword=_x \
	--language=java \
	--no-location \
	--no-wrap \
	--output=../text/original.pot \
	--package-name=RegexPlanet \
	--package-version='' \
	--sort-output

for f in ../text/*.po
do
	msgmerge --update $f ../text/original.pot
done

rm *.tmp
