# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 09:15:32 2024

@author: Thijssenj

Search Functions
"""

import re

def check_tashkeel(text: str) -> bool:
    pattern = re.compile('[\u0617-\u061A\u064B-\u0652]')
    
    return len(pattern.findall(text)) > 0


def remove_tashkeel(text: str) -> str:
    # Define a regular expression pattern to match diacritics
    pattern = re.compile('[\u0617-\u061A\u064B-\u0652]')
    
    # Use the sub() method to replace matched diacritics with an empty string
    text = re.sub(pattern, '', text)
    
    return text

def root_search(word, quran) -> list:
    pattern = re.compile(r'\b\w*{}\w*\b'.format(re.escape(word)))
    
    # Find all matches in the text
    matches = pattern.findall(quran)
    
    return matches

def root_dictionary(word, quran) -> dict:
    matches = root_search(word, quran)
    
    result = {}
    for word in matches:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    return result

def find_and_label_root(word, quran) -> dict:
    filtered_instances = []
    for no, surah in enumerate(quran, start=1):
        for verse_num, ayah in enumerate(surah, start=1):
            pattern = re.compile(r'\b\w*{}\w*\b'.format(re.escape(word)))
            matches = pattern.findall(ayah)

            for match in matches:
                filtered_instances.append((no, verse_num, match))
    return filtered_instances