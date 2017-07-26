# -*- coding: utf-8 -*-

from .base_csv_dao import BaseCsvDao


class TvChannelsCsvDao(BaseCsvDao):

    def __init__(self, path):
        super(TvChannelsCsvDao, self).__init__(path)

        self.dataFile = 'channels'
        self.columnNames = ['ChannelId', 'Position', 'Definition', 'Abbreviation', 'Title']


    def get_channel_id(self, channelPosition):
        return self.data.iloc[channelPosition, 0]

