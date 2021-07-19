#!/usr/bin/env python3

import host
import os
import sys
import sqlite3
import random
import re
from datetime import datetime
from time import sleep

quantity_words = int(sys.argv[1])
my_new_dict = []

def download_db():
    update = input('Скачать БД? yes/no   ')
    if update == 'yes':
        if 'en_to_ru.db' in os.listdir():
            os.remove('en_to_ru.db')
        os.system(f'wget -c {host.address}/cgi-bin/my_dictionary/en_to_ru.db')
    else:
        pass

class MyDict():
    """Этот класс создаёт my_dict из en_to_ru.db и
       определяет методы для работы с ним."""
    def __init__(self):
        self.db = sqlite3.connect('en_to_ru.db')
        self.curs = self.db.cursor()
        self.my_old_dict = sorted(self.curs.execute("select * from dictionary;").fetchall())
        self.curs.close()
        self.db.close()

    def request_translate_ru_en(self):
        """Создаёт запрос на перевод случайно выбранного русского слова, 
и добавляет запись в новом словаре (для отслеживания незапомненных слов)."""
        self.word = random.choice(self.my_old_dict)
        self.ru_w = self.word[1]
        self.en_w = self.word[0]
        self.sign = self.word[2]
        self.response = input(f'Переведи это слово:   {self.ru_w}\n')
        self.response_re = re.search(self.response, self.en_w)
        if self.response_re:
            self.my_version_en_w = self.response_re.group()
            if bool(self.my_version_en_w) and self.my_version_en_w in self.en_w:
                my_new_dict.append([self.en_w, [self.ru_w, 1]])
            else:
                my_new_dict.append([self.en_w, [self.ru_w, 0]])
        else:
            my_new_dict.append([self.en_w, [self.ru_w, 0]])
        self.d = datetime.now()
        self.time = self.d.strftime("%H:%M:%S")
        self.str_for_log = f'{self.time}   Моя версия ==> {self.my_version_en_w}; на самом деле ==> {self.en_w}'
        sleep(1)
        print(self.str_for_log)
        print('')
        return self.str_for_log

class Log():
    """Этот класс пишет лог сессии в файл '<date_time>.log'."""
    def __init__(self):
        self.name_log = f'{datetime.now().strftime("%d-%m-%Y_%H-%M")}.log'
        if self.name_log not in os.listdir():
           self.log = open(f'{self.name_log}', 'w')
           self.log.close()

    def write_log(self, s):
        with open(f'{self.name_log}', 'a') as self.log:
            self.log.write(f'{s}\n')

try:
    #download_db() # раскомментить

    my_dict = MyDict()
    log = Log()

    if quantity_words >= len(my_dict.my_old_dict):
        quantity_words = len(my_dict.my_old_dict)

    for i in range(quantity_words):
        my_dict.request_translate_ru_en() # возращаемая str_for_log каждый раз новая
        log.write_log(my_dict.str_for_log)
except re.error:
    print('Были введены некорректные символы!')
except (KeyboardInterrupt, SystemExit):
    exit()
finally:
    print('')
    print(f'my_new_dict ==> {my_new_dict}')
