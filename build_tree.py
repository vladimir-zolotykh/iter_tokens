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
        res: None = BinaryOperator(left=self.term())
        while self._accept(PT.Plus) or self._accept(PT.Minus):
            right: Node = BinaryOperator(right=self.term())
            res.right = (
                right
                if not res.right
                else BinaryOperator(type(self.tok), left=res, right=right)
            )
        return res

    def term(self) -> Node:
        res: None = BinaryOperator(left=self.factor())
        while self._accept(PT.Times) or self._accept(PT.Divide):
            # op = type(self.tok)
            right: Node = Node(right=self.factor())
            res.right = (
                right
                if not res.right
                else BinaryOperator(type(self.tok), left=res, right=right)
            )
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
    def setUp(self):
        self.t = NodeTree()

    def test_10_expr(self):
        self.assertEqual(self.t.build("2 + 3"), 5)
        # self.assertEqual(self.t.build("3 + 4 * 5"), 23)
        # self.assertEqual(self.t.build("2 + (3 + 4) * 5"), 37)
        # with self.assertRaises(SyntaxError):
        #     self.t.build("2 + (3 + * 4)")


if __name__ == "__main__":
    unittest.main()
