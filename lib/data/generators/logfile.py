# -*- coding: utf-8 -*-

import io


class LogFileGenerator(object):
    def __init__(self, size, rubbish):
        self.size = size
        self.rubbish = rubbish

        self.BLOCK_SIZE = 1000
        self.FILE_EXT = ".log"


    def run(self, filename):
        filename = filename + self.FILE_EXT
        self.generatedLines = 0
        with io.open(filename, "w+", encoding='utf-8') as f:
            lines = self.get_lines()
            f.write(lines)



