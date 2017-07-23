# -*- coding: utf-8 -*-

import uuid
from .base_generator import BaseGenerator


class CustomerGenerator(BaseGenerator):
    def __init__(self, size):
        super(CustomerGenerator, self).__init__(size)
        self.FILE_EXT = ".csv"


    def get_line(self):
        return uuid.uuid4().hex


