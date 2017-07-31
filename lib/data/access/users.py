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

        self.exponentialVariateLambdaValue = 1 / setSample

        self.generate_randomized_users()
        return self


#    @time_profiler
    def generate_randomized_users(self):
        random_values = np.random.exponential(self.exponentialVariateLambdaValue, self.RANDOM_BLOCK_SIZE)
        floored = [math.floor(r) for r in random_values]
        self.randomizedUsers = [ str( self.data.iloc[pos][0] ) for pos in floored]
        self.userPointer = 0

    
    # @time_profiler
    # def randomize_users(self):
    #     self.randomizedUsers = []
    #     for i in range(1000):
    #         self.randomizedUsers.append(self.fetch_random_user())


    # @mass_profiler
    # def fetch_random_user(self): 
    #     pos = math.floor(random.expovariate(self.exponentialVariateLambdaValue) )
    #     pos = min(pos, self.dataSize-1)
    #     #print('User', pos, type(self.data.iloc[pos]), self.data.iloc[pos], "\nA:", str(self.data.iloc[pos][0]))
    #     return str(self.data.iloc[pos][0])
    #     #return self.data.iloc[pos] 'UserId']


#    @mass_profiler
    def get_random_user(self):
        if self.userPointer >= self.RANDOM_BLOCK_SIZE:
            #self.generate_randomized_users()
            self.userPointer = 0

        element = self.randomizedUsers[self.userPointer]
        self.userPointer+= 1
        return element


