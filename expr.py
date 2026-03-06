from abc import ABC, abstractmethod

from tokens import Token


class Visitor(ABC):
    @abstractmethod
    def visit_binary(self, expr: "Binary") -> object:
        pass

    @abstractmethod
    def visit_grouping(self, expr: "Grouping") -> object:
        pass

    @abstractmethod
    def visit_literal(self, expr: "Literal") -> object:
        pass

    @abstractmethod
    def visit_unary(self, expr: "Unary") -> object:
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> object:
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        super().__init__()

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_binary(self)


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_grouping(self)


class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()

        self.value = value

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_literal(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        super().__init__()

        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_unary(self)
