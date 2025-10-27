#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re
from typing import NamedTuple, Any, Iterator
import unittest

NUM = r"(?P<NUM>\d+)"
MINUS = r"(?P<MINUS>-)"
PLUS = r"(?P<PLUS>\+)"
DIVIDE = r"(?P<DIVIDE>/)"
TIMES = r"(?P<TIMES>\*)"
LPAREN = r"(?P<LPAREN>\()"
RPAREN = r"(?P<RPAREN>\))"
WS = r"(?P<WS>\s+)"


class Token(NamedTuple):
    name: str
    value: Any


master_pat = re.compile("|".join([NUM, DIVIDE, PLUS, MINUS, TIMES, LPAREN, RPAREN, WS]))


def iter_tokens(text: str) -> Iterator[Token]:
    for m in re.finditer(master_pat, text):
        token = Token(m.lastgroup, m.group())
        if token.name == "WS":
            continue
        yield token


class TestParse(unittest.TestCase):
    def test_10_base(self):
        self.assertEqual(
            [tok.name for tok in list(iter_tokens("3 + 4 * 5"))],
            ["NUM", "PLUS", "NUM", "TIMES", "NUM"],
        )


if __name__ == "__main__":
    unittest.main()
