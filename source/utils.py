'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Various helper functions to make the processing of jisho search
                results easier or more readable.
'''
import re

# Checks if a character is Hiragana, returning true if yes and false otherwise
def isHiragana(c):
    return True if 0x3041 <= ord(c) and ord(c) <= 0x3096 else False

# Checks if a character is Katakana, returning true if yes and false otherwise
def isKatakana(c):
    return True if 0x30a1 <= ord(c) and ord(c) <= 0x30ff else False

# Checks if a character is Hiragana or Katakana, returning true if yes and
# false otherwise
def isKana(c):
    return True if isHiragana(c) or isKatakana(c) else False

# Returns only kana from a word
def kana(word):
    allKana = ""
    for jpnchar in word:
        if isKana(jpnchar):
            allKana += jpnchar
    return allKana

# Returns only okurigana from a word
def kanji(word):
    # remove all strings within square brackets, and remove the square brackets
    return re.sub("[\[].*?[\]]", "", word).replace(" ", "")
