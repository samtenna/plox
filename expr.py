from abc import ABC, abstractmethod

from tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept[T](visitor: Visitor[T]) -> T:
        pass


class Visitor(ABC):
    pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        super().__init__()

        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression


class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()

        self.value = value


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        super().__init__()

        self.operator = operator
        self.right = right
