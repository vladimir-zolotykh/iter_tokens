#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, cast
import unittest
import parse_tokens as PT
import visitor as VI


class Node:
    pass


class BinaryOperator(Node):
    def __init__(
        self,
        operator: PT.Operator,
        left: Node,
        right: Node,
    ) -> None:
        self.operator = operator
        self.left = left
        self.right = right


class Num(Node):
    def __init__(self, val: int):
        self.val = val


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
            op = cast(PT.Operator, type(self.tok))
            right: Node = self.term()
            res = BinaryOperator(op, left=res, right=right)
        return res

    def term(self) -> Node:
        res: Node = self.factor()
        while self._accept(PT.Times) or self._accept(PT.Divide):
            op = cast(PT.Operator, type(self.tok))
            right: Node = self.factor()
            res = BinaryOperator(op, left=res, right=right)
        return res

    def factor(self) -> Node:
        if self._accept(PT.Num):
            tok: PT.Num = cast(PT.Num, self.tok)
            return Num(int(tok.value))
        elif self._accept(PT.Lparen):
            res: Node = self.expr()
            self._expect(PT.Rparen)
            return res
        else:
            raise SyntaxError(f"Expected {PT.Num} or {PT.Lparen}")


class TestEvaluate(unittest.TestCase):
    maxDiff = None  # disables truncation

    def setUp(self):
        self.t = NodeTree()
        self.vi = VI.Evaluate()
        self.lisp = VI.Lisp()

    def test_10_expr(self):
        self.assertEqual(self.vi.visit(self.t.build("2 + 3")), 5)
        self.assertEqual(self.lisp.visit(self.t.build("2 + 3")), "(+ 2 3)")

    def test_20_expr(self):
        self.assertEqual(self.vi.visit(self.t.build("2 + 3 * 4")), 14)
        self.assertEqual(self.lisp.visit(self.t.build("2 + 3 * 4")), "(+ 2 (* 3 4))")

    def test_30_expr(self):
        self.assertEqual(self.vi.visit(self.t.build("2 + (3 + 4) * 5")), 37)
        self.assertEqual(
            self.lisp.visit(self.t.build("2 + (3 + 4) * 5")), "(+ 2 (* (+ 3 4) 5))"
        )

    def test_40_expr(self):
        with self.assertRaises(SyntaxError):
            self.vi.visit(self.t.build("2 + (3 + * 4)"))
        with self.assertRaises(SyntaxError):
            self.lisp.visit(self.t.build("2 + (3 + * 4)"))


if __name__ == "__main__":
    unittest.main()
