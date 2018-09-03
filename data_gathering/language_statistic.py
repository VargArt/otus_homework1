import re
import pandas as pd


def language_statistic(posts):

    key_words = {'c++': 0, 'python': 0, 'java': 0, 'go': 0}

    posts['text'].fillna('nan\n', inplace=True)

    for text_post in posts['text']:
        a = re.search('\s[Cc][+][+]\s', text_post)
        if a is not None:
            key_words['c++'] += 1
        a = re.search('\s[Pp]ython\s', text_post)
        if a is not None:
            key_words['python'] += 1
        a = re.search('\s[Jj]ava\s', text_post)
        if a is not None:
            key_words['java'] += 1
        a = re.search('\s[Gg]o\s', text_post)
        if a is not None:
            key_words['go'] += 1

    for key, val in key_words.items():
        print('Язык', key, 'упоминается в', val, 'постах')