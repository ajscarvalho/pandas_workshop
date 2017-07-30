# -*- coding: utf-8 -*-

from .base_csv_dao import BaseCsvDao


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


    def load(self):
        super(UsersCsvDao, self).load()

        self.channels = self.data['ChannelId'].unique() # or load channels separatelly

        self.dataSize = self.channels.shape[0] # 100? 200?
        setSample = self.dataSize * 0.1 # 10% 

        self.exponentialVariateLambdaValue = 1 / setSample


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
        self.currentTimeFrame = self.data[self.data['StartDate'] <= startDate && startDate < self.data['EndDate'] ].groupby("ChannelId")#.copy()


    def get_random_event(self):
        channelPos = floor(random.expovariate(self.exponentialVariateLambdaValue) )
        channelId = self.channels[channelPos]
        return self.currentTimeFrame[channelId]


    def get_event_date_limits(self):
        return '2017-01-02 00:00:00', max(self.data['StartDate']) + ' 23:59:59'
