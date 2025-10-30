#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import build_tree as BT
import parse_tokens as PT
import operator


class Visitor:
    def visit(self, node: BT.Node):
        method_name: str = "visit_" + type(node).__name__
        try:
            method = getattr(self, method_name)
        except AttributeError:
            method = self.visit_generic
        return method(node)

    def visit_generic(self, node):
        raise TypeError(f"No visit method of {node} found")


class Evaluate(Visitor):
    def visit_Num(self, node: BT.Num) -> int:
        return int(node.val)

    def visit_BinaryOperator(self, node: BT.BinaryOperator) -> int:
        op = {
            PT.Plus: operator.add,
            PT.Minus: operator.sub,
            PT.Times: operator.mul,
            PT.Divide: operator.floordiv,
        }[node.operator]
        res = op(self.visit(node.left), self.visit(node.right))
        return res


class Lisp(Visitor):
    def visit_Num(self, node) -> str:
        return str(node.val)

    def visit_BinaryOperator(self, node: BT.BinaryOperator) -> str:
        op = {
            PT.Plus: "+",
            PT.Minus: "-",
            PT.Times: "*",
            PT.Divide: "//",
        }[node.operator]
        res = f"({op} {self.visit(node.left)} {self.visit(node.right)})"
        return res
