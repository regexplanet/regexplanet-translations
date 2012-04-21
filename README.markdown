# regexplanet-translations

These are the translation strings for [RegexPlanet](http://www.regexplanet.com/).

## Notes to translators

If a *MsgId* starts with `%`, then look in the English translation (en.po) for the text.

If a *MsgId* ends with `.html`, then the text can contain HTML, and must be safe to embed in a webpage as-is.

## New Translations

If you are starting a new translation from scratch (i.e. creating a brand new .po file), you must put the metadata lines at the top.  The .po files contain UTF-8 strings, so you specifically need the following lines:

    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"

See the original.pot or en.po for complete examples.
