# -*- coding: utf-8 -*-

from .base_csv_dao import BaseCsvDao


class EpgProgramsCsvDao(BaseCsvDao):

    def __init__(self, path):
        super(EpgProgramsCsvDao, self).__init__(path)

        self.dataFile = 'programs'
        self.columnDataTypes = {
            'SeriesId': str,
            'SeriesSeason': str,
            'SeriesEpisode': str
        }


    def get_random_id(self):
        return self.data.sample().iloc[0]['ProgramId']


