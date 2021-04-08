'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Class for processing Jisho search results.
'''

import sys
import requests
from bs4 import BeautifulSoup
from utils import isKana

class WordSearch:
    def __init__(self, searched_word):
        self.cur_word, self.max_words, self.page = 0, 0, 0
        self.word_tag, self.primary_tag = None, None
        self.word_dict = {}
        self.all_words = []
        self.error_msg = "No error."
        self.error_code = 0
        # format searched word for url, i.e. searching "to run #word" should
        # really be "to%20run%20%23word"
        self.searched_word = searched_word.replace(' ', '%20').replace('#', '%23')
        self.check_search()
        self.load_data()
    
    def get_soup(self):
        # inc page and load webpage data
        self.page += 1
        url = "https://jisho.org/search/" + self.searched_word + '?page=' + str(self.page)
        webpage = requests.get(url)
        if webpage.status_code != 200:
            sys.exit("Error: There was an issue loading Jisho. Try again later.")
        soup = BeautifulSoup(webpage.content, "html.parser")
        return soup

    def check_search(self):
        # if new search, try getting results
        if self.max_words == 0:
            self.primary_tag = self.get_soup().find('div', id='primary')
            if self.primary_tag is None:
                self.error_msg = 'Error: No results.  Please try again.'
                self.error_code = 1
            else:
                new_words = list(self.primary_tag.find_all('div', class_='concept_light clearfix'))
                self.all_words.extend(new_words)
                self.max_words += len(new_words)
        # if the current word is the last word on the page, try getting the next page
        elif self.cur_word == self.max_words - 1:
            if self.primary_tag.find('a', class_='more') is not None:
                self.primary_tag = self.get_soup().find('div', id='primary')
                if self.primary_tag is not None:
                    new_words = list(self.primary_tag.find_all('div', class_='concept_light clearfix'))
                    self.all_words.extend(new_words)
                    self.max_words += len(new_words)

    def get_word_and_reading(self):
        final_word = ""
        word_info = self.word_tag.find('div', class_='concept_light-representation')
        # list comprehension to extract whole word as string
        word = "".join([text.get_text().strip() for text in \
            word_info.find_all('span', class_='text')])
        # list comprehension to extract kanji readings (furigana on Jisho)
        furigana = [furi.get_text().strip() for furi in \
            word_info.find('span', class_='furigana').find_all('span')]
        
        # count number of kanji in the word and number of non-empty
        # furigana instances
        num_kanji, num_furi = 0, 0
        for char in word:
            if not isKana(char):
                num_kanji += 1
        for furi in furigana:
            if furi:
                num_furi += 1
        
        # weird ruby version of furigana tag that crashed my program once
        if word_info.find('ruby', class_='furigana-justify') is not None:
            all_ruby = word_info.find('ruby', class_='furigana-justify').findChildren()
            for child in all_ruby:
                if child.name != 'rb' and child.name != 'rt':
                    final_word += child.get_text().strip()
                elif child.name == 'rt':
                    final_word += " %s" % child.previous_sibling.get_text().strip()
                    final_word += "[%s]" % (child.get_text().strip())
        elif len(word) == len(furigana) and num_kanji == num_furi:
            for cur in range(len(word)):
                # append current char if hiragana, and append kanji reading otherwise
                final_word += " %s[%s]" % (word[cur], furigana[cur]) if not isKana(word[cur]) else word[cur]
        # update error to reflect weird jisho formatting and attempt to create a correct reading
        else:
            self.error_code = 4
            self.error_msg = "Warning: Jisho furigana formatting error."
            try:
                final_word += "%s[%s]" % (word, "".join(furigana))
            except:
                final_word = word
        if len(final_word) > 0 and final_word[0] == " ":
            final_word = final_word[1:]
        final_word = final_word.replace("[]", "")
        self.word_dict['Word'] = final_word
    
    def get_word_info(self):
        self.word_tag_info = self.word_tag.find('div', class_='concept_light-status')
        # get all tags, like wanikani level, common word y/n, and JLPT level
        tags = [tag.get_text().strip() for tag in \
                self.word_tag_info.find_all('span', class_='concept_light-tag')]
        self.word_dict['Common'] = ''
        self.word_dict['JLPT'] = 'N/A'
        for tag in tags:
            if tag.find('Common') != -1:
                self.word_dict['Common'] = 'Common word<br>'
            if tag.find('JLPT') != -1:
                self.word_dict['JLPT'] = 'N' + tag.split(" ")[1][1]
    
    def get_word_meanings(self):
        meanings_dict = {}
        meanings_list = []
        # get the parent meaning tag, called meanings-wrapper
        meanings_info = self.word_tag.find('div', class_='meanings-wrapper')
        # get all meanings and parts of speech for each meaning
        meanings_children = meanings_info.findChildren('div', class_='meaning-wrapper', \
                                                       recursive=False)
        for child in meanings_children:
            meanings_dict = {'Meaning(s)': '', 'Tags': 'N/A'}
            meaning = child.find('span', class_='meaning-meaning')
            if meaning is not None:
                meanings_dict['Meaning(s)'] = meaning.get_text().strip()
            else:
                continue
            # some words are labeled with parts of speech and some aren't, so
            # check for a part of speech
            if child.previous_sibling is not None and child.previous_sibling.has_attr('class') \
               and child.previous_sibling['class'][0] == 'meaning-tags':
               # ignore wikipedia definitions
                if child.previous_sibling.get_text().strip().find('Wikipedia') != -1:
                    continue
                meanings_dict['Tags'] = child.previous_sibling.get_text().strip()
            meanings_list.append(meanings_dict)
        self.word_dict['Meanings'] = meanings_list
    
    def next_word(self):
        self.error_msg = "No error."
        self.error_code = 0
        self.check_search()
        # increment buffer if cur_word is not pointing to the head of the array
        if self.cur_word < self.max_words - 1:
            self.cur_word += 1
        else:
            self.error_msg = "Error: Cannot go forward."
            self.error_code = 3
        self.load_data()
    
    def prev_word(self):
        self.error_msg = "No error."
        self.error_code = 0
        # decrement buffer if possible
        if self.cur_word > 0:
            self.cur_word -= 1
        else:
            self.error_msg = "Error: Cannot go back."
            self.error_code = 2
        self.load_data()

    def load_data(self):
        # make sure index is not out of bounds
        if self.cur_word >= 0 and self.cur_word < self.max_words:
            self.word_dict = {}
            self.word_tag = self.all_words[self.cur_word]
            self.get_word_and_reading()
            self.get_word_info()
            self.get_word_meanings()

if __name__ == '__main__':
    # Problematic words: unubore, hung
    jisho_word = WordSearch('tasty')
    for i in range(43):
        jisho_word.next_word()
    for i in range(45):
        jisho_word.next_word()
    for i in range(3):
        jisho_word.prev_word()
    for i in range(42):
        jisho_word.next_word()
    for i in range(5):
        jisho_word.next_word()