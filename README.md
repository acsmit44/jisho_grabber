# jisho_grabber: A Program for Creating Anki Notes from Jisho

`jisho_grabber` allows the user to enter a search word, select a result, select one of the result's definitions, and add it to their Anki deck.

*This program and its author are not affiliated with the main Anki project or Jisho.org in any way.*

## Dependencies

This program was written in Python version 3.8.5.  It depends on four Python libraries: BeautifulSoup4, requests, wxPython, and [genanki](https://github.com/kerrickstaley/genanki).  BeautifulSoup4, requests, and wxPython can be installed with a simple `pip install {library name}` command on both Windows and Linux.  Installing genanki is very simple as well.  First, clone the repository.  Then, on Linux, cd into the repository directory and use `make` to run the Makefile, which will do the work for you.  On Windows, open a Powershell window as admin, cd into the repository directory, and run the command `python setup.py install --user` to install (or `python3` depending on your command shortcut).

## Missing Features

- For now, there is only one style of Anki deck available and it is hard-coded in.  It contains all fields of information that this program is currently capable of extracting from Jisho.  I may be adding custom Note and Model creation in the future, but doing so strays away from the primary focus of this program.
- Example sentences and additional information do not get added to the cards.  This might be a feature that I will implement once this program is fully-functional with the base features.

## Important Notes

Please note that my search program literally looks up the word as it is typed in, and that the program is only built to handle *words* and not kanji searches.  Because of the way jisho's website is formatted, the method of grabbing kanji information is different from word information.  Additionally, note that Jisho's search engine will attempt to interpret words written in the English alphabet as romaji.  For example, if you search the word fun, Jisho will convert it to ふん and search for that instead.  To remedy this, one must search with quotation marks, such as "fun".