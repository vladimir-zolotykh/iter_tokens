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


class TokenMeta(type):
    _registry: dict = {}

    def __init__(cls, name, bases, ns):
        super().__init__(name, bases, ns)
        TokenMeta._registry.setdefault(cls, set())
        for base in bases:
            if isinstance(base, TokenMeta):
                TokenMeta._registry.setdefault(base, set()).add(cls)
        TokenMeta._update_leaves()

    @classmethod
    def _update_leaves(mcls):
        mcls.leaves = {
            c.__name__.upper(): c for c, subs in mcls._registry.items() if not subs
        }


@dataclass
class Token(metaclass=TokenMeta):
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


master_pat = re.compile("|".join([NUM, DIVIDE, PLUS, MINUS, TIMES, LPAREN, RPAREN, WS]))


def iter_tokens(text: str) -> Iterator[Token]:
    for m in re.finditer(master_pat, text):
        token = Token.leaves[m.lastgroup](m.lastgroup, m.group())
        if token.name == "WS":
            continue
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
    # print(TokenMeta.leaves)
    unittest.main()
