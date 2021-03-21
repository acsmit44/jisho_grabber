'''
Author:         Andrew Smith
Project:        Jisho grabber
Description:    Main script for processing Jisho search results and otputting
                them in a readable and convenient way.
'''

import sys
import requests
from bs4 import BeautifulSoup
from utils import isKana

'''
Takes a url and returns the HTML content unless there is a server error.
'''
def get_soup(url):
    page = requests.get(url)
    if page.status_code != 200:
        sys.exit("Error: There was an issue loading Jisho. Try again later.")
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

'''
Takes in an instance of a concept_light clearfix div HTML tag and extracts the
whole word as well as the reading of the word.
'''
def get_word_and_reading(word_tag, word_dict):
    word_info = word_tag.find('div', class_='concept_light-representation')
    # list comprehension to extract whole word as string
    word = "".join([text.get_text().strip() for text in
                       word_info.find_all('span', class_='text')])
    # list comprehension to extract kanji readings
    furigana = [furi.get_text().strip() for furi in \
                word_info.find('span', class_='furigana').find_all('span')]
    reading = ""
    for cur in range(len(word)):
        # append current char if hiragana, and append kanji reading otherwise
        reading += word[cur] if isKana(word[cur]) else furigana[cur]
    word_dict['Word'] = word
    word_dict['Reading'] = reading

'''
Takes in an instance of a concept_light clearfix div HTML tag and extracts the
word tag information, such as whether it is a common word and what level it is
in the JLPT.
'''
def get_word_info(word_tag, word_dict):
    word_tag_info = word_tag.find('div', class_='concept_light-status')
    tags = [tag.get_text().strip() for tag in \
            word_tag_info.find_all('span', class_='concept_light-tag')]
    word_dict['Common word'] = 'No'
    word_dict['JLPT'] = 'N/A'
    for tag in tags:
        if tag.find('Common word') != -1:
            word_dict['Common word'] = 'Yes'
        if tag.find('JLPT') != -1:
            word_dict['JLPT'] = tag.split(" ")[1][1]

'''
Takes in an instance of a concept_light clearfix div HTML tag and extracts the
parts of speech and definitions for each meaning.
'''
def get_word_meanings(word_tag, word_dict):
    meanings_info = word_tag.find('div', class_='meanings-wrapper')
    meaning_tags = [tag.get_text().strip() for tag in \
                    meanings_info.find_all('div', class_='meaning-tags')]
    meanings = [tag.get_text().strip() for tag in \
                meanings_info.find_all('span', class_='meaning-meaning')]
    meanings_list = []
    for cur in range(len(meanings)):
        # ignore wikipedia definitions
        # TODO: Fix this since there will not always be as many meanings as tags
        if meaning_tags[cur].find('Wikipedia') != -1:
            continue
        meanings_list.append({'Part(s) of speech' : meaning_tags[cur], \
                              'Meaning(s)' : meanings[cur]})
    word_dict['Meanings'] = meanings_list

'''
Extract all useful information from each result.
'''
def process_word(word_tag):
    word_dict = {}
    get_word_and_reading(word_tag, word_dict)
    get_word_info(word_tag, word_dict)
    get_word_meanings(word_tag, word_dict)
    return word_dict

'''
Top-level function that goes through each result in the page, extracts each
word's information, and adds it to a list.
'''
def process_search_results(searched_word):
    all_words = []
    searched_word = searched_word.replace(' ', '%20').replace('#', '%23')
    results = get_soup("https://jisho.org/search/" + searched_word)
    primary_tag = results.find('div', id='primary')
    word_results = primary_tag.find_all('div', class_='concept_light clearfix')
    for word_result in word_results:
        all_words.append(process_word(word_result))
    return all_words

results = get_soup("https://jisho.org/search/" + searched_word)
primary_tag = results.find('div', id='primary')
word_tag = primary_tag.find('div', class_='concept_light clearfix')

# request page and parse html
all_words = process_search_results("best friend #word")
test = 1