# RegexPlanet Translations

These are the translation strings for [RegexPlanet](http://www.regexplanet.com/).  The scripts used are all in the `bin` directory.

## Notes to translators

If a *MsgId* starts with `%`, then it is a macro.  Look in the English translation (en.po) for the text.

If a *MsgId* ends with `.html`, then the text can contain HTML, and must be safe to embed in a webpage as-is.

Entries with the `fuzzy` flag set are from Google Translate.  If you fix one (or if by some stroke of luck it is correct), unset it.  Once there are no more fuzzy entries,  I can change the `%html.lang.attribute` to the raw language code.  This is necessary to comply with [Google Translate's terms of service](https://developers.google.com/translate/v2/markup).

## New translations

If you are starting a new translation from scratch (i.e. creating a brand new .po file), you must put the metadata lines at the top.  The .po files contain UTF-8 strings, so you specifically need the following lines:

    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"

See the original.pot or en.po for complete examples.

## Workflow

This is the workflow that

 # run `extract.sh`.  This creates the `original.pot` with all the strings that have to be translated, and adds blank entries to all the `XX.po` files for new strings.
 # run `gtrans.sh`.  This fills in any blank entries in the `XX.po` files with a machine translation.
 # Human translators edit the `XX.po` files and update all the `fuzzy` entries.
 # run `process.sh`.  This transfers the text in the `XX.po` files back to the website.

## Credits

[polib](https://bitbucket.org/izi/polib/wiki/Home) - python library to deal with .po file format from David Jean Louis

[Google Translate](http://translate.google.com/) - for machine translation
