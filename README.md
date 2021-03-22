# jisho_grabber: A Program for Creating Anki Notes from Jisho Searches

`jisho_grabber` allows the user to enter a search word, select a result, select one of the result's definitions, and add it to their Anki deck with the click of a button (okay, four buttons, but you get the idea).

*This program and its author are not affiliated with the main Anki project or Jisho.org in any way.*

## Motivation

Up until winter of 2020, I always had a hard time studying Japanese.  Finding the motivation to learn new vocab and whatnot never came easy to me, despite the fact that I'd say I'm passionate about learning Japanese.  I knew about Anki, but didn't seriously start using it until that winter.  When I finally created some decks for vocab, studying became significantly easier.  Along with vocabulary, I also created a deck (a subset of [this all-in-one kanji deck](https://ankiweb.net/shared/info/798002504)) of all kanji with frequency rankings of 1-2500.  In addition to rote memorization, I also began studying by reading and watching some stuff in Japanese without aid such as subtitles.  During my reading or watching, I would frequently came across a word that felt significant enough to search on Jisho.  Whether it was because it came up often, or it felt familiar, or because I straight-up had no idea what the hell it meant and couldn't help but look, I found myself searching with *great* frequency.  However, here's how searching one of said words on Jisho always went:
*Hears word* "Oh that seems important, I should look it up" -> *Searches word* "Wow cool, I'll have to remember this word and its meaning" -> 1 min pass -> Word forgotten -> repeat
Maybe the *one* exception to this is 変身する, which is a suru-verb meaning "to transform"/"to shapeshift", and the only reason I can remember this one is because they say it like 20 times an episode in the season of [Precure](https://anilist.co/anime/603/) that I'm watching right now.
Because of this, I decided to code a Chrome extension that would let me select a word on a Jisho page and turn it into an Anki note.  Turns out Chrome's API is garbage, the documentation is comically outdated, there is hardly anyone talking about Chrome extensions on StackExchange, and I didn't want to figure out how to convert raw text into Anki notes anyway.  Because of this, I decided to not code a Chrome extension that would let me select a word on a Jisho page and turn it into an Anki note.
And then it hit me.  Why don't I just make my own GUI that displays Jisho search results?  That way, I could just make my own interface and decide how it works.  Plus, I had just discovered a python library that can dump a bunch of info into an Anki note.
Anyway, long story short, I wrote this program because I'm too lazy to take the 15 seconds to search a word and then manually input a new note into Anki.  That is why I spent 50 hours over the last 5 days writing a program that would cut that time down from 15 seconds to 10.

## Dependencies

This program was written in Python version 3.8.5.  It depends on four Python libraries: BeautifulSoup4, requests, wxPython, and [genanki](https://github.com/kerrickstaley/genanki).  BeautifulSoup4, requests, and wxPython can be installed with a simple `pip install {library name}` command on both Windows (I used PowerShell and it worked just fine) and Linux/Mac.  Installing genanki is very simple as well.  First, clone the repository.  Then, on Linux/Mac, cd into the repository directory and use `make` to run the Makefile, which will do the work for you.  On Windows, open a Powershell window as admin, cd into the repository directory, and run the command `python setup.py install --user` to install (or `python3` depending on your command shortcut).

## Missing Features

- For now, there is only one style of Anki deck available and it is hard-coded in.  It contains all fields of information that this program is currently capable of extracting from Jisho.  I may be adding custom Note and Model creation in the future, but doing so strays away from the primary focus of this program, which is just a quick-and-dirty way of creating Anki notes from Jisho word searches.
- Example sentences and additional information do not get added to the cards.  This might be a feature that I will implement once this program is fully-functional with the base features.

## Important Notes

Please note that my search program literally looks up the word as it is typed in, and that the program is only built to handle *words* and not kanji searches.  Because of the way jisho's website is formatted, the method of grabbing kanji information is different from word information.  Additionally, note that Jisho's search engine will try its darndest to interpret words written in the English alphabet as romaji.  For example, if you search the word fun, Jisho will convert it to ふん and search for that instead.  To remedy this, one must search with quotation marks, such as "fun".