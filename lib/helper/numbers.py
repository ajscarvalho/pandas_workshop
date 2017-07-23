# -*- coding: utf-8 -*-


def human_readable_int_to_machine(size):
    """ translates human readable integer format to integer
        @param str Number that may optionally end with K, M, or G at
            the end, to ease writting powers of ten
        @return int
    """
    multiplier = 1
    size = size.upper()
    if   size[-1] == 'K': multiplier = 1000
    elif size[-1] == 'M': multiplier = 1000000
    elif size[-1] == 'G': multiplier = 1000000000

    if multiplier > 1: size = size[:-1]
    size = int(size)
    return size * multiplier

