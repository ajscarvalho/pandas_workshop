# -*- coding: utf-8 -*-

import io
from datetime import datetime
import random

from .base_generator import BaseGenerator
from helper.random_select import random_select_list

#from helper.time_profiler import print_report, mass_profiler


class LogFileGenerator(BaseGenerator):

    def __init__(self, usersDao, eventsDao, wordList, size, rubbish):
        self.usersDao   = usersDao
        self.eventsDao  = eventsDao
        self.wordList   = wordList

        self.rubbish    = rubbish
        self.recordCount = size / (1-rubbish)
        self.size = self.recordCount

        print ("Generating", self.recordCount, "Records")

        self.BLOCK_SIZE = 10000
        self.FILE_EXT = ".log"

        self.GOOD_EVENT = 'ChangeChannel'
        self.OTHER_EVENT_TYPES = ['TimeWarp', 'VOD', 'StbOn', 'StbOff', 'HDMI_On', 'HDMI_Off', 'Garbage']
        self.EVENT_TEMPLATES = {
            'ChangeChannel' : '{timestamp}:{garbage1} User@{user}: {eventName}({channelId}, {eventId}, {fakeId}) {garbage2}',
            'TimeWarp'      : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'VOD'           : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'StbOn'         : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'StbOff'        : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'HDMI_On'       : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'HDMI_Off'      : '{timestamp}:{garbage1} User@{user}: {eventName}({fakeId}) {garbage2}',
            'Garbage'       : '{timestamp}:{garbage1} {fakeId} {garbage2}',
        }

        self.DIGITS = '1234567890'

        #event crawling
        self.dateFormat = '%Y-%m-%d %H:%M:%S'
        
        dateLimits = eventsDao.get_event_date_limits()
        self.currentTS  = datetime.strptime(dateLimits[0], self.dateFormat).timestamp()
        self.endTS      = datetime.strptime(dateLimits[1], self.dateFormat).timestamp()
        self.ts_step    = (self.endTS - self.currentTS) / self.recordCount

        self.timeframeEnd = self.currentTS


#    @mass_profiler
    def get_line(self):
        good = random.random() > self.rubbish

        eventName = self.GOOD_EVENT if good else random.choice(self.OTHER_EVENT_TYPES)
        timestamp = self.get_timestamp()
        garbage1  = self.get_garbage(['.'], 5)
        garbage2  = self.get_garbage(['., :;+-*/&%$#@!_'], 3)
        fakeId    = self.get_fake_id(eventName, '.-:/_', 4, 8)
        user = self.usersDao.get_random_user()
    
        # create line
        line = self.EVENT_TEMPLATES[eventName]
        line = line.replace('{timestamp}', timestamp)
        line = line.replace('{user}', user)
        line = line.replace('{eventName}', user)

        line = line.replace('{garbage1}', garbage1)
        line = line.replace('{garbage2}', garbage2)
        line = line.replace('{fakeId}', fakeId)

        if good:
            event = self.eventsDao.get_random_event()
            #print (event)
            line = line.replace('{channelId}', event.ChannelId)
            line = line.replace('{eventId}', event.EventId)

        return line


    def get_garbage(self, seplist, maxWords):
        garbage = ''
        wordList = list(random_select_list(self.wordList,   minimum=1,  maximum=maxWords))

        for word in wordList:
            if garbage: garbage+= random.choice(seplist)
            garbage += word

        return garbage


    def get_fake_id(self, eventName, sepList, minDigits, maxDigits):
        digitCount = random.randint(minDigits, maxDigits)
        digits = []
        for i in range(digitCount):
            digits.append(random.choice(self.DIGITS))
        return '{}{}{}'.format( eventName[0], random.choice(sepList), ''.join(digits) )


    def get_timestamp(self):
        self.currentTS += self.ts_step
        if self.currentTS > self.endTS: raise StopIteration

        if self.currentTS > self.timeframeEnd:
            self.advance_time_frame()

        tsStr = datetime.fromtimestamp(self.currentTS).strftime(self.dateFormat)
        return tsStr


    def advance_time_frame(self):
        datetimeStr = datetime.fromtimestamp(self.timeframeEnd).strftime(self.dateFormat)
        self.eventsDao.select_time_frame(datetimeStr) # will become startDate
        self.timeframeEnd += 300 #5 minutes
        #print_report()


