#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import unittest
import parse_tokens as PT


class Node:
    pass


class BinaryOperator(Node):
    def __init__(
        self,
        operator: PT.Operator = type(None),
        left: Node | None = None,
        right: Node | None = None,
    ) -> None:
        self.operator = (operator,)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOperator({self.operator}, {self.left}, {self.right})"


class Num(Node):
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f"Num({self.val})"


class NodeTree:
    tok: PT.Token | None = None  # current token
    tok_next: PT.Token | None = None  # next (look-ahead) token
    tokens: Iterator[PT.Token]

    def _advance(self) -> None:
        self.tok, self.tok_next = self.tok_next, next(self.tokens, None)

    def _accept(self, tok_type: type[PT.Token]) -> bool:
        if isinstance(self.tok_next, tok_type):
            self._advance()
            return True
        return False

    def _expect(self, tok_type: type[PT.Token]) -> None:
        if not self._accept(tok_type):
            raise SyntaxError(f"Expected {tok_type}")

    def build(self, text):
        self.tokens = PT.iter_tokens(text)
        self._advance()
        return self.expr()

    def expr(self) -> Node:
        res: Node = self.term()
        while self._accept(PT.Plus) or self._accept(PT.Minus):
            op = type(self.tok)
            right: Node = self.term()
            res = BinaryOperator(op, left=res, right=right)
        return res

    def term(self) -> Node:
        res: None = self.factor()
        while self._accept(PT.Times) or self._accept(PT.Divide):
            op = type(self.tok)
            right: Node = self.factor()
            res = BinaryOperator(op, left=res, right=right)
        return res

    def factor(self) -> Node:
        if self._accept(PT.Num):
            return Num(int(self.tok.value))
        elif self._accept(PT.Lparen):
            res: Node = self.expr()
            self._expect(PT.Rparen)
            return res
        else:
            raise SyntaxError(f"Expected {PT.Num} or {PT.Lparen}")


class TestNodeTree(unittest.TestCase):
    maxDiff = None  # disables truncation

    def setUp(self):
        self.t = NodeTree()

    def test_10_expr(self):
        self.assertEqual(
            repr(self.t.build("2 + 3")),
            "BinaryOperator((<class 'parse_tokens.Plus'>,), Num(2), Num(3))",
        )
        self.assertEqual(
            repr(self.t.build("3 + 4 * 5")),
            (
                "BinaryOperator((<class 'parse_tokens.Plus'>,), Num(3), "
                "BinaryOperator((<class 'parse_tokens.Times'>,), Num(4), Num(5)))"
            ),
        )
        self.assertEqual(
            repr(self.t.build("2 + (3 + 4) * 5")),
            (
                "BinaryOperator((<class 'parse_tokens.Plus'>,), Num(2), "
                "BinaryOperator((<class 'parse_tokens.Times'>,), "
                "BinaryOperator((<class 'parse_tokens.Plus'>,), Num(3), Num(4)), Num(5)))"
            ),
        )
        with self.assertRaises(SyntaxError):
            self.t.build("2 + (3 + * 4)")


if __name__ == "__main__":
    unittest.main()
