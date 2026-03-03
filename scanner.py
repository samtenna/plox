from logger import Logger
from tokens import Token, TokenType

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self._add_token(TokenType.EOF)
        return self.tokens

    def _scan_token(self):
        c = self._advance()

        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "/":
                if self._match("/"):
                    # Comment until the end of the line
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)

            # Whitespace
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1

            # Literals
            case '"':
                self._string()

            case _:
                if c.isdigit():
                    self._number()
                elif c.isalpha():
                    self._identifier()
                else:
                    Logger.error(self.line, "Unexpected character.")

    def _identifier(self):
        while self._peek().isalnum():
            self._advance()

        text = self.source[self.start : self.current]
        type = KEYWORDS.get(text)
        if not type:
            type = TokenType.IDENTIFIER

        self._add_token(type)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()

            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            Logger.error(self.line, "Unterminated string.")
            return

        self._advance()

        val = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, val)

    def _peek(self):
        if self._is_at_end():
            return "\0"

        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def _match(self, expected: str):
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _add_token(self, type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _advance(self):
        if not self._is_at_end():
            self.current += 1

        return self.source[self.current - 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)
