import argparse

from ast_printer import AstPrinter
from expr import Binary, Grouping, Literal, Unary
from parser import Parser
from scanner import Scanner
from tokens import Token, TokenType


class PLox:
    def __init__(self):
        self.had_error = False

    def _run_repl(self):
        while True:
            line = input("> ")
            self._run(line)

            self.had_error = False

    def _run_file(self, file_name: str):
        with open(file_name, "r") as f:
            contents = f.read()
            self._run(contents)

        if self.had_error:
            exit(1)

    def _run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if self.had_error or not expression:
            return

        print(AstPrinter().print(expression))


if __name__ == "__main__":
    interpreter = PLox()
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()

    # expr = Binary(
    #     Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    #     Token(TokenType.STAR, "*", None, 1),
    #     Grouping(Literal(45.67)),
    # )

    # print(AstPrinter().print(expr))

    if not args.file:
        interpreter._run_repl()
    else:
        print("Running file")
