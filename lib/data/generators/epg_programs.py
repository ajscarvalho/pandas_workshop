# -*- coding: utf-8 -*-

import random
from .base_generator import BaseGenerator

from configuration.epg_refdata import Config as EpgRefData

from helper.random_select import random_select_list
from helper.text import canonicalize

class ProgramsGenerator(BaseGenerator):

    def __init__(self, wordList, size):
        super(ProgramsGenerator, self).__init__(size)

        self.wordList = wordList

        self.FILE_EXT = ".csv"
        self.BLOCK_SIZE = size

        self.recurrentRatio = 0.7
        self.seriesRatio = 0.2
        self.recurrentThreshold = self.recurrentRatio
        self.seriesThreshold = self.recurrentThreshold + self.seriesRatio
        #moviesRatio = remaining = 0.1,  moviesThreshold = remaining = 1

        self.episodesPerSeriesAvg = 10
        self.liveRate = 0.05

        self.programIdGen = 1
        self.seriesDict = set()
        self.cache = {}


    def get_line(self):
        self.programIdGen +=1
        progId          = "{:7d}".format(self.programIdGen)
        progType        = self.choose_program_type()
        progName        = self.generate_program_name(progType)
        progGenre       = self.choose_genres()
        progActors      = self.choose_actors    (progType, progName)
        progDirectors   = self.choose_directors (progType, progName)
        progRating      = self.choose_rating()
        progYear        = self.choose_year()
        progDesc        = self.choose_description()
        seriesId        = self.choose_series_id(progType, progName)
        seriesSeason    = self.choose_series_season(progType)
        seriesEpisode   = self.choose_series_episode(progType)
        
        return '{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:2.2f},{:s},{:s},{:s},{:s},{:s}'.format(
            progId, 
            progType[0], 
            progType[1], 
            progName.title(), 
            '*'.join(progGenre), 
            '*'.join(progActors), 
            '*'.join(progDirectors),
            progRating,
            progYear,
            progDesc,
            seriesId,
            seriesSeason,
            seriesEpisode
        )


    def choose_program_type(self):
        rnd = random.random()
        if rnd <= self.recurrentThreshold:
            programType = 'RECURRENT'
        elif rnd <= self.seriesThreshold:
            programType = 'SERIES'
        else:
            programType = 'MOVIE'
        
        isLive = 'LIVE' if rnd <= self.liveRate else ''

        return (programType, isLive)


    def generate_program_name(self, progType):
        possibleName = self.choose_name()
        if progType[0] == 'SERIES':
            avgSeriesEpisodes = self.size * self.seriesRatio
            avgSeries = avgSeriesEpisodes / self.episodesPerSeriesAvg

            seriesCount = len(self.seriesDict)
            reuseProb = seriesCount / avgSeries
            if random.random() <= reuseProb:
                reused = random.sample(self.seriesDict, 1)[0]
                return reused

            self.seriesDict.add(possibleName)

        return possibleName


    def choose_genres(self):
        return random_select_list(EpgRefData['genres'], maximum=4)

    # a decorator would make sense here
    def choose_actors(self, progType, progName):
        cachekey = 'actors_t:' + '_'.join(progType) + '_p:' + progName;
        existing = self.cache.get(cachekey)
        if existing: return existing 
        
        newEntry = random_select_list(EpgRefData['actors'], minimum=0,  maximum=5)
        self.cache[cachekey] = newEntry
        return newEntry


    def choose_directors(self, progType, progName):
        cachekey = 'directors_t:' + '_'.join(progType) + '_p:' + progName;
        existing = self.cache.get(cachekey)
        if existing: return existing 
        
        newEntry = random_select_list(EpgRefData['directors'], minimum=0,  maximum=2)
        self.cache[cachekey] = newEntry
        return newEntry


    def choose_rating(self): return 10 * random.random()
    def choose_year(self): return str(2000 + random.randint(0, 17))

    def choose_name(self):
        wordList = random_select_list(self.wordList,   minimum=2,  maximum=5)
        return ' '.join(wordList)

    def choose_description(self): 
        wordList = random_select_list(self.wordList,   minimum=5,  maximum=20)
        return ' '.join(wordList) + '.'


    def choose_series_id(self, progType, progName):
        if progType[0] != 'SERIES': return ''
        return canonicalize(progName)


    def choose_series_season(self, progType):
        if progType[0] != 'SERIES': return ''
        return str(random.randint(1, 40))

    def choose_series_episode(self, progType):
        if progType[0] != 'SERIES': return ''
        return str(random.randint(100, 900))
