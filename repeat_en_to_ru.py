#!/usr/bin/env python3

import os
import sqlite3
import random
import subprocess
import json
from time import sleep
from datetime import datetime

period = int(input("Время паузы:   "))
print("\n")
termux_values = []


def result_termux_query(termux_values):
    subprocess.call('./.termux_query.sh')
    result_file = open('.result_termux_query.txt','r')
    result = json.load(result_file)
    for i in range(len(result)):
        termux_values.append(result[i]['text'])
    return termux_values

def date_time():
    date = datetime.now()
    time = date.strftime("%d/%m/%Y %H:%M:%S")
    return time

if 'en_to_ru.db' in os.listdir():
    os.system('rm en_to_ru.db')

os.system('wget -c http://www.ieroglif1977.ru/cgi-bin/my_dictionary/en_to_ru.db')

db = sqlite3.connect('en_to_ru.db')
curs = db.cursor()
my_dict = sorted(curs.execute('select * from dictionary;').fetchall())

repeated_words = []
for i in range(len(my_dict)):
    if my_dict[i][2] == 1:
        repeated_words.append(my_dict[i])

curs.close(); del curs
db.close(); del db

random.shuffle(repeated_words)

def repeat():
    result_termux_query(termux_values)
    
    print(f'{date_time()}')
    print(f'Всего в словаре {len(my_dict)} слов.')
    print(f'Повторяемых слов:   {len(repeated_words)}')
    print('\n')
    for i in range(len(repeated_words)):
        sleep(period)
        print(f'{i+1}. {repeated_words[i][0]} ==> {repeated_words[i][1]}')
        if 'termux-toast' in termux_values:
            os.system(f'termux-toast -g top -b green -c black {i+1}. {repeated_words[i][0]}')
        if 'termux-tts-speak' in termux_values:
            os.system(f'termux-tts-speak -p 0.8 -r 0.8 {repeated_words[i][0]}')
    print('\n')
    print(f'{date_time()}\nThe dictionary ended.')
    if 'termux-toast' in termux_values:
        os.system('termux-toast -g top -b green -c black "The dictionary ended."')
    if 'termux-tts-speak' in termux_values:
        os.system('termux-tts-speak -p 0.8 -r 0.8 "The dictionary ended."')

try:
    repeat()
except KeyboardInterrupt:
    exit()
