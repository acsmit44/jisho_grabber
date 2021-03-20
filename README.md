# jisho_grabber: A Program for Creating Anki Notes from Jisho

`jisho_grabber` allows the user to enter a search word, select a result, select one of the result's definitions, and add it to their Anki deck.

*This program and its author are not affiliated with the main Anki project or Jisho.org in any way.*

## Dependencies

This program was written in Python version 3.8.5.  It depends on three Python libraries: BeautifulSoup4, requests, and [genanki](https://github.com/kerrickstaley/genanki).  BeautifulSoup4 and requests can be installed with a simple `pip install beautifulsoup4` and `pip install requests` command on both Windows and Linux.  Installing genanki is very simple as well.  First, clone the repository.  Then, on Linux, one can simply use `make` to run the Makefile, which will do the work for you.  On Windows, open a Powershell window as admin and run the command `python setup.py install --user` to install (or `python3` depending on your command shortcut).

## Missing Features

As of now, there is only one style of Anki deck available and it is hard-coded in.  It contains all fields of information that this program is currently capable of extracting from Jisho.  I may be adding custom Note and Model creation in the future, but doing so strays away from the primary focus of this program.