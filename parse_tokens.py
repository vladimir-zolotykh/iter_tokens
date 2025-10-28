#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from typing import NamedTuple, Any, Iterator
from dataclasses import dataclass
import unittest

NUM = r"(?P<NUM>\d+)"
MINUS = r"(?P<MINUS>-)"
PLUS = r"(?P<PLUS>\+)"
DIVIDE = r"(?P<DIVIDE>/)"
TIMES = r"(?P<TIMES>\*)"
LPAREN = r"(?P<LPAREN>\()"
RPAREN = r"(?P<RPAREN>\))"
WS = r"(?P<WS>\s+)"


@dataclass
class Token:
    name: str
    value: Any


@dataclass
class Num(Token):
    def __post_init__(self):
        self.value = int(self.value)


@dataclass
class Operator(Token):
    def __repr__(self):
        return str(self.value)


@dataclass
class Plus(Operator):
    pass


@dataclass
class Minus(Operator):
    pass


@dataclass
class Times(Operator):
    pass


@dataclass
class Divide(Operator):
    pass


@dataclass
class Lparen(Token):
    pass


@dataclass
class Rparent(Token):
    pass


@dataclass
class Ws(Token):
    pass


def find_leaves(base_class: type = Token) -> list[type]:
    leaves: set(type) = set()

    def recurse(cls):
        subs = cls.__subclasses__()
        if not subs:
            leaves.add(cls)
        else:
            for sub in subs:
                recurse(sub)

    recurse(base_class)
    return leaves


TOKENS = find_leaves(Token)
master_pat = re.compile("|".join([NUM, DIVIDE, PLUS, MINUS, TIMES, LPAREN, RPAREN, WS]))


def iter_tokens(text: str) -> Iterator[Token]:
    for m in re.finditer(master_pat, text):
        if m.lastgroup == "WS":
            continue
        token_cls = type(None)
        for cls in TOKENS:
            if cls.__name__.upper() == m.lastgroup:
                token_cls = cls
                break
        token = token_cls(m.lastgroup, m.group())
        yield token


class TestParse(unittest.TestCase):
    def test_10_base(self):
        self.assertEqual(
            ["NUM", "PLUS", "NUM", "TIMES", "NUM"],
            [tok.name for tok in list(iter_tokens("3 + 4 * 5"))],
        )
        self.assertEqual(
            [3, "+", 4, "*", 5],
            [tok.value for tok in list(iter_tokens("3 + 4 * 5"))],
        )


if __name__ == "__main__":
    unittest.main()
