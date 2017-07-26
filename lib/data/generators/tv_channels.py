# -*- coding: utf-8 -*-

import random
from .base_generator import BaseGenerator

from helper.random_select import random_select_list


class TvChannelsGenerator(BaseGenerator):

    def __init__(self, wordList, size):
        super(TvChannelsGenerator, self).__init__(size)

        self.wordList = wordList

        self.FILE_EXT = ".csv"
        self.BLOCK_SIZE = size

        self.CHARLIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.CHARLEN = len(self.CHARLIST)
        self.CHANNELLEN = 4

        self.hdRate = 0.1
        self.channelPosition = 0
        self.channelId = random.randint(0, 5)

        self.channelAbbrevs = set()


    def get_line(self):
        self.channelPosition+= random.randint(1, 5)
        self.channelId += random.randint(1, 5)

        isHd = random.random() <= self.hdRate
        channelType = 'HD' if isHd else 'SD'

        wordList = list(random_select_list(self.wordList,   minimum=1,  maximum=5))
        channelTitle = ' '.join(wordList).title()
        channelAbbrev = self.generate_channel_abbrev(wordList)

        return 'C-{:04d},{:d},{:s},{:s},{:s}'.format(
            self.channelId, self.channelPosition, channelType, channelAbbrev, channelTitle
        )


    def generate_channel_abbrev(self, titleWords):
        minimumLetters = 3
        titleWordCount = len(titleWords) 
        abbrev = [''] * titleWordCount
        run = 1
        titlePos = 0
        letters = 0

        for i in range(titleWordCount):
            abbrev[i] = titleWords[i][0].upper()
            letters+= 1

        while letters < minimumLetters:
            letters+= 1
            try:
                nextLetter = titleWords[titlePos][run]
            except:
                nextLetter = self.get_random_char()

            abbrev[titlePos] += nextLetter

            titlePos += 1
            if titlePos >= titleWordCount:
                titlePos = 0
                run += 1

        result = ''.join(abbrev)

        while result in self.channelAbbrevs:
            result += self.get_random_char()

        self.channelAbbrevs.add(result)

        return result


    def get_random_char(self):
        return self.CHARLIST[random.randint(0, self.CHARLEN-1)] 

    def generate_channel_title(self):
        wordList = random_select_list(self.wordList,   minimum=1,  maximum=5)

        