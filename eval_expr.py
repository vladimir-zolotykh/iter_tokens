#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import parse_tokens as PT


class Evaluator:
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

    def parse(self, text):
        self.tok: PT.Token | None = None  # current token
        self.tok_next: PT.Token | None = None  # next (look-ahead) token
        self.tokens = PT.iter_tokens(text)
        self._advance()
        return self.expr()

    def expr(self):
        res = self.term()
        while self._accept(PT.Plus) or self._accept(PT.Minus):
            op = self.tok.type
            right = self.term()
            if op == PT.Plus:
                res += right
            else:
                res -= right
        return res

    def term(self):
        res = self.factor()
        while self._accept(PT.Times) or self._accept(PT.Divide):
            op = self.tok.type
            right = self.factor()
            if op == PT.Times:
                res *= right
            else:
                res /= right
        return res

    def factor(self):
        if self._accept(PT.Num):
            return int(self.tok.value)
        elif self._accept(PT.Lparen):
            res = self.expr()
            self._expect(PT.Rparen)
            return res
        else:
            raise SyntaxError(f"Expected {PT.Num} or {PT.Lparen}")
