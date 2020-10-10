import functools
import random
import unicodedata

import redbaron


__all__ = ['alternatives', 'substitute', 'rewrite']


__version__ = '0.4'


identifier_start_categories = [
    'Lu',
    'Ll',
    'Lt',
    'Lm',
    'Lo',
    'Nl',
]

identifier_continue_categories = [
    *identifier_start_categories,
    'Mn',
    'Mc',
    'Nd',
    'Pc',
]


@functools.lru_cache
def alternatives(char, start=True):
    identifier_categories = identifier_start_categories if start else identifier_continue_categories

    normal = unicodedata.normalize('NFKC', char)
    alts = []

    for idx in range(0, 65536):
        ch = chr(idx)
        if unicodedata.category(ch) in identifier_categories and unicodedata.normalize('NFKC', ch) == normal:
            alts.append(ch)

    if not alts:
        return [char]
    else:
        return alts


def substitute(identifier, *, extra_safe=False):
    normal = unicodedata.normalize('NFKC', identifier)
    subbed = []

    if extra_safe:
        subbed.append(normal[0])
    else:
        subbed.append(random.choice(alternatives(normal[0], True)))
    for char in normal[1:]:
        subbed.append(random.choice(alternatives(char, extra_safe)))

    return ''.join(subbed)


def rewrite(source):
    fst = redbaron.RedBaron(unicodedata.normalize('NFKC', source))

    for node in fst.find_all('namenode'):
        node.value = substitute(node.value)

    for node in fst.find_all('nameasnamenode'):
        node.value = substitute(node.value, extra_safe=True)

    for node in fst.find_all('defnode'):
        node.name = substitute(node.name)

    for node in fst.find_all('classnode'):
        node.name = substitute(node.name)

    return fst.dumps()
