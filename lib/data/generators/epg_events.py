# -*- coding: utf-8 -*-

import random
import sys
from .base_generator import BaseGenerator

#from helper.random_select import random_select_list
#from helper.text import canonicalize


class EventsGenerator(BaseGenerator):

    def __init__(self, channelsDao, programsDao, days):
        super(EventsGenerator, self).__init__(sys.maxsize) # set to a big number and when the last channel is set set size to 0

        if days > 30: days = 30

        self.channelsDao = channelsDao
        self.programsDao = programsDao

        self.FILE_EXT = ".csv"
        self.BLOCK_SIZE = sys.maxsize
        print('maxsize', sys.maxsize)

        self.totalDays = days

        self.dates = ['2017-01-{:02d}'.format(d) for d in range(1, days+1)]

        self.eventId = random.randint(100000, 999999) # initial eventId is random with 6 digits

        self.durations = [5, 10, 15, 20, 30, 45, 60, 75, 90, 120, 150, 180]
        self.startTimes = ['22:00', '22:20', '22:30', '22:40', '23:00', '23:30', '23:45', '23:50', '00:00', '00:05']

        self.currentDay         = 0
        self.currentChannelPos  = 0
        self.currentChannelId   = None
        self.currentStartTime   = None
        self.currentEndTime     = None

        self.channelStartTimes = {}

        self.totalChannels = len(self.channelsDao)
        self.writeNow = False


    def end(self): self.size = 0


    def force_write(self):   self.writeNow = True
    def prevent_write(self): self.writeNow = False
    def terminate_lines_block(self): return self.writeNow


    def get_line(self):
        self.prevent_write()
        line = self.create_event()

        #step
        if self.no_more_time_slots(): self.next_channel()
        else:                         self.next_time_slot()

        if self.no_more_channels(): self.next_day()
        
        if self.no_more_days    (): self.end()

                
        return line

    
    def create_event(self):
        self.eventId += 1
        if self.currentChannelId is None: self.currentChannelId = self.get_channel_id()
        if self.currentStartTime is None: self.currentStartTime = self.initialize_time()
        duration = self.select_random_duration()
        self.currentEndTime = self.add_duration_to_time(duration)
        #self.currentChannelId
        programId = self.select_random_program_id()

        startDate   = self.format_start_date()
        endDate     = self.format_end_date()

        event = 'E/{:08d},{:s},{:s},{:d},{:s},{:s}'.format(
            self.eventId, self.currentChannelId, programId, duration, startDate, endDate)
        
        return event


    def next_time_slot(self): self.currentStartTime = self.currentEndTime

    def next_channel(self): 
        #save time in channel start times hash
        self.channelStartTimes[self.currentChannelId] = self.currentEndTime

        # advance channel
        self.currentChannelPos+= 1
        self.currentChannelId  = None
        self.force_write() # write to disk

    def next_day(self):
        """advance day and reset channel pointer"""
        self.currentDay+= 1 
        self.currentChannelPos = 0
        self.currentChannelId  = None


    def no_more_channels    (self): return self.currentChannelPos   >= self.totalChannels
    def no_more_days        (self): return self.currentDay          >= self.totalDays

    def no_more_time_slots  (self):
        return self.currentStartTime and self.currentEndTime and self.currentEndTime < self.currentStartTime


    def initialize_time(self):
        time = self.channelStartTimes.get(self.currentChannelId)
        if time: return time
        
        return random.choice(self.startTimes)


    def get_channel_id(self):
        return self.channelsDao.get_channel_id(self.currentChannelPos)