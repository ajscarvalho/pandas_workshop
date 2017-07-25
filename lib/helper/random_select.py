# -*- coding: utf-8 -*-

import random


def random_select_list(lst, minimum=1, maximum=1):
    elements = {}

    elemCount = minimum
    if minimum != maximum:
        elemCount = random.randint(minimum, maximum)

    while len(elements) < elemCount:
        element = random.choice(lst)
        elements[element] = 1

    return elements.keys()
