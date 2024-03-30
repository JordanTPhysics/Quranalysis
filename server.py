# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 07:57:14 2024

@author: Thijssenj
"""

from flask import Flask, request, jsonify, render_template
import asyncio
from datasource import quran_datasource
import search as qs
from flask_cors import CORS


quran = None
server = Flask(__name__)
CORS(server)

@server.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@server.route('/api/surah/<int:number>', methods=['GET'])
def surah_text(number):
    return quran[['Chapter', 'normal']].iloc[number-1].to_dict()

@server.route('/api/rootsearch/<string:word>', methods=['GET'])
def rootsearch(word):
    
    word = qs.remove_tashkeel(word)
    book = quran['noTashkeel'].tolist()
    
    return qs.find_and_label_root(word, book)

if __name__ == '__main__':
    quran = quran_datasource()
    server.run(debug=False, port=8000)