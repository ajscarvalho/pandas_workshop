# -*- coding: utf-8 -*-

from .base_csv_dao import BaseCsvDao


class TvChannelsCsvDao(BaseCsvDao):

    def __init__(self, path):
        super(TvChannelsDAO, self).__init__(path)

        self.dataFile = 'channels'


