import functools
import random
import unicodedata

import libcst


__all__ = ['alternatives', 'substitute', 'rewrite']


__version__ = '0.5.1'


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


def substitute(identifier):
    normal = unicodedata.normalize('NFKC', identifier)
    subbed = []

    subbed.append(random.choice(alternatives(normal[0], True)))
    for char in normal[1:]:
        subbed.append(random.choice(alternatives(char)))

    return ''.join(subbed)


class SubstituteTransformer(libcst.CSTTransformer):
    def leave_Name(self, original_node, updated_node):
        return updated_node.with_changes(value=substitute(updated_node.value))


def rewrite(source):
    cst = libcst.parse_module(source)

    transformer = SubstituteTransformer()

    cursed_cst = cst.visit(transformer)

    return cursed_cst.code
