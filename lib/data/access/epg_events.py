# -*- coding: utf-8 -*-

import random
import math
import numpy as np

from .base_csv_dao import BaseCsvDao

#from helper.time_profiler import time_profiler, mass_profiler


class EpgEventsCsvDao(BaseCsvDao):

    def __init__(self, path):
        super(EpgEventsCsvDao, self).__init__(path)

        self.dataFile = 'events'
        self.columnNames = 'EventId,ChannelId,ProgramId,Duration,StartDate,EndDate'.split(',')
        self.columnDataTypes = {
            'EventId':      str,
            'ChannelId':    str,
            'ProgramId':    str,
            'Duration':     int,
            'StartDate':    str,
            'EndDate':      str
        }

        self.randomizedChannels = []
        self.RANDOM_BLOCK_SIZE = 5000 #0.5 s
        self.channelPointer = self.RANDOM_BLOCK_SIZE + 1


    def load(self):
        super(EpgEventsCsvDao, self).load()

        self.channels = self.data['ChannelId'].unique() # or load channels separatelly

        self.dataSize = self.channels.shape[0] # 100? 200?
        setSample = self.dataSize * 0.1 # 10% 

        self.exponentialVariateLambdaValue = 1 / setSample

        self.generate_randomized_channels()

        return self


    # @param    00:05 00:10#
    #           Start   End     Result
    # @record   00:00   00:05   Out
    # @record   00:00   00:10   In
    # @record   00:00   00:15   In
    # @record   00:05   00:10   In
    # @record   00:05   00:15   In
    # @record   00:10   00:15   Out
    def select_time_frame(self, startDate):
        """consider always a 5m period and always aligned to 5m intervals"""
        print ("Changing TimeFrame to ", startDate)
        filtered = self.data[(self.data['StartDate'] <= startDate) & (startDate < self.data['EndDate']) ].copy()
        self.currentTimeFrame = filtered.set_index("ChannelId", drop=False).copy()
        self.eventCache = {}



    #@time_profiler
    def generate_randomized_channels(self):
        random_values = np.random.exponential(self.exponentialVariateLambdaValue, self.RANDOM_BLOCK_SIZE)
        floored = [math.floor(r) for r in random_values]
        self.randomizedChannels = [ str( self.channels[pos] ) for pos in floored]
        self.channelPointer = 0


    #@mass_profiler
    def get_random_channel(self):
        if self.channelPointer >= self.RANDOM_BLOCK_SIZE:
            #self.generate_randomized_channels()
            self.channelPointer = 0

        element = self.randomizedChannels[self.channelPointer]
        self.channelPointer+= 1
        return element


    #@mass_profiler
    def get_random_event(self):
        #channelPos = math.floor(random.expovariate(self.exponentialVariateLambdaValue) )
        #channelPos = math.floor(np.random.exponential(self.exponentialVariateLambdaValue, self.dataSize) )
        #channelId = self.channels[channelPos]
        channelId = self.get_random_channel()
        #cache
        cachedEvent = self.eventCache.get(channelId)
        if cachedEvent is not None: return cachedEvent
        
        event = self.currentTimeFrame.ix[channelId]
        self.eventCache[channelId] = event
        return event


    def get_event_date_limits(self):
        return '2017-01-02 00:00:00', max(self.data['StartDate'])[0:10] + ' 23:59:59'
