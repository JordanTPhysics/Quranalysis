# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 08:14:41 2024

@author: Thijssenj
"""

import nltk, re, numpy as np, pandas as pd

import string
from snowballstemmer import stemmer
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates
import os

from util import QURAN_CHAPTERS as titles
from search import find_and_label_root, remove_tashkeel
FIG_SIZE = (10, 15)

def quran_datasource():

    quran = pd.read_csv('quran-simple.txt', sep="|", header=None)
    quran.columns = ['Surah', 'Ayah', 'Content']
    quran.drop(quran.index[6236:], inplace=True)
    quran['Surah'] = pd.to_numeric(quran['Surah'], downcast = 'integer')
    quran['Ayah'] = pd.to_numeric(quran['Ayah'], downcast = 'integer')
    
    surah_ayat = quran.groupby('Surah')['Content'].apply(list).tolist()
    ayahs_no_tash = quran.groupby('Surah')['Content'].apply(lambda s: list([remove_tashkeel(x) for x in s])).tolist()
    surahs = [' '.join(surah) for surah in surah_ayat]
    surahs_no_tash = list(map(remove_tashkeel, surahs))

    return pd.DataFrame({'Chapter': titles,
                              'noTashkeel': ayahs_no_tash,
                              'normal': surah_ayat,
                              'noTashkeel_joined': surahs_no_tash,
                              'normal_joined': surahs})

quran = quran_datasource()
number = 5
surah = quran.iloc[number-1].to_dict()

res = find_and_label_root('بسم',quran['noTashkeel'])
