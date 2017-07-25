# -*- coding: utf-8 -*-

import io, os

def get_words(rootPath):
    filename = os.path.join(rootPath, 'refdata', 'en_50k.txt')
    with io.open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        words = [l.split(' ')[0] for l in lines]

    return words

