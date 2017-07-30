# -*- coding: utf-8 -*-

from .base_csv_dao import BaseCsvDao

import random

class UsersCsvDao(BaseCsvDao):

    def __init__(self, path, commonUserPct=0.2):
        super(UsersCsvDao, self).__init__(path)

        self.dataFile = 'users'
        self.columnNames = ['UserId']
        self.columnDataTypes = {
            'UserId': str,
        }

        self.commonUserPct = commonUserPct


    def load(self):
        super(UsersCsvDao, self).load()

        self.dataSize = self.data.shape[0] # 10K
        setSample = self.dataSize * 0.2

        self.exponentialVariateLambdaValue = 1 / setSample


    def get_random_user(self): 
        pos = floor(random.expovariate(self.exponentialVariateLambdaValue) )
        pos = min(pos, self.dataSize) 
        return self.data.iloc[pos]['UserId']


