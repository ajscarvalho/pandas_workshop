# -*- coding: utf-8 -*-

import random
import math
import numpy as np

from .base_csv_dao import BaseCsvDao

#from helper.time_profiler import time_profiler, mass_profiler


class UsersCsvDao(BaseCsvDao):

    def __init__(self, path, commonUserPct=0.2):
        super(UsersCsvDao, self).__init__(path)

        self.dataFile = 'customers'
        self.columnNames = ['UserId']
        self.columnDataTypes = {
            'UserId': str,
        }

        self.commonUserPct = commonUserPct

        self.randomizedUsers = []
        self.RANDOM_BLOCK_SIZE = 50000 # 1000 => 0.1 s, 50k => 5s
        self.userPointer = self.RANDOM_BLOCK_SIZE + 1


    def load(self):
        super(UsersCsvDao, self).load()

        self.dataSize = self.data.shape[0] # 10K
        setSample = self.dataSize * 0.2

        self.exponentialVariateLambdaValue = setSample / 2

        self.generate_randomized_users()
        return self


#    @time_profiler
    def generate_randomized_users(self):
        random_values = np.random.exponential(self.exponentialVariateLambdaValue, self.RANDOM_BLOCK_SIZE)
        floored = [math.floor(r) for r in random_values]
        self.randomizedUsers = [ self.select_user_at_pos(pos) for pos in floored]
        self.userPointer = 0


    def select_user_at_pos(self, pos):
        size = len(self.data)
        if pos >= size:
            #print('Offlimits', pos, 'in', size)
            pos = np.random.randint(0, size - 1)

        return str( self.data.iloc[pos][0] )


#    @mass_profiler
    def get_random_user(self):
        if self.userPointer >= self.RANDOM_BLOCK_SIZE:
            #self.generate_randomized_users()
            self.userPointer = 0

        element = self.randomizedUsers[self.userPointer]
        self.userPointer+= 1
        return element


