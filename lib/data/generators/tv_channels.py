# -*- coding: utf-8 -*-

import random
from .base_generator import BaseGenerator


class TvChannelsGenerator(BaseGenerator):

    def __init__(self, size):
        super(TvChannelsGenerator, self).__init__(size)
        self.FILE_EXT = ".csv"
        self.BLOCK_SIZE = size

        self.CHARLIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.CHARLEN = len(self.CHARLIST)
        self.CHANNELLEN = 4

        self.hdRate = 0.1
        self.channelPosition = 0


    def get_line(self):
        self.channelPosition+= 1
        isHd = random.random() <= self.hdRate
        channelType = 'HD' if isHd else 'SD'
        channelName = self.generateChannelName()
        return '{},{},{}'.format(self.channelPosition, channelType, channelName)


    def generateChannelName(self):
        s = ''
        for i in range(self.CHANNELLEN):
            s += self.CHARLIST[random.randint(0, self.CHARLEN-1)]

        return s


