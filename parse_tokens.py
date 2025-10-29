#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from typing import Any, Iterator, ClassVar, reveal_type
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
    re: ClassVar[str] = ""


@dataclass
class Num(Token):
    re = r"(?P<NUM>\d+)"

    def __post_init__(self):
        self.value = int(self.value)


@dataclass
class Operator(Token):
    def __repr__(self):
        return str(self.value)


@dataclass
class Plus(Operator):
    re = r"(?P<PLUS>\+)"


@dataclass
class Minus(Operator):
    re = r"(?P<MINUS>-)"


@dataclass
class Times(Operator):
    re = r"(?P<TIMES>\*)"


@dataclass
class Divide(Operator):
    re = r"(?P<DIVIDE>/)"


@dataclass
class Lparen(Token):
    re = r"(?P<LPAREN>\()"


@dataclass
class Rparen(Token):
    re = r"(?P<RPAREN>\))"


@dataclass
class Ws(Token):
    re = r"(?P<WS>\s+)"


def find_leaves(base_class: type[Token] = Token) -> set[type[Token]]:
    leaves: set[type[Token]] = set()

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
master_pat = re.compile("|".join([cls.re for cls in TOKENS]))


def iter_tokens(text: str) -> Iterator[Token]:
    for m in re.finditer(master_pat, text):
        if m.lastgroup == "WS":
            continue
        # token_cls: type[Token] | type[None] = type(None)
        for cls in TOKENS:
            if cls.__name__.upper() == m.lastgroup:
                token_cls = cls
                break
        # reveal_type(token_cls)
        if token_cls is not type(None) and m.lastgroup:
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
