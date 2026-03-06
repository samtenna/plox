from expr import Binary, Expr, Grouping, Literal, Unary, Visitor


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary(self, expr: Binary) -> str:
        return self._parenthesise(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self._parenthesise("group", expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesise(expr.operator.lexeme, expr.right)

    def _parenthesise(self, name: str, *exprs: Expr):
        string = f"({name} "

        for expr in exprs:
            string += f" {expr.accept(self)}"

        string += ")"

        return string
