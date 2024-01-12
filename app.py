import re

class Lexer:
    def __init__(self, input_text):
        self.tokens = re.findall(r'\d+|[-+*/()]|[a-zA-Z_]\w*|\s+', input_text)
        self.current = 0

    def get_next_token(self):
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            self.current += 1
            return token
        return None

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        return self._expression()

    def _expression(self):
        term = self._term()
        while True:
            op = self.lexer.get_next_token()
            if op in ('+', '-'):
                term = term + self._term() if op == '+' else term - self._term()
            else:
                self.lexer.current -= 1
                break
        return term

    def _term(self):
        factor = self._factor()
        while True:
            op = self.lexer.get_next_token()
            if op in ('*', '/'):
                factor = factor * self._factor() if op == '*' else factor / self._factor()
            else:
                self.lexer.current -= 1
                break
        return factor

    def _factor(self):
        token = self.lexer.get_next_token()
        if token.isdigit():
            return int(token)
        elif token.isalpha():
            return 0 
        elif token == '(':
            result = self._expression()
            if self.lexer.get_next_token() != ')':
                raise SyntaxError("Mismatched parentheses")
            return result
        else:
            raise SyntaxError("Invalid token: {}".format(token))

class CalculatorInterpreter:
    def evaluate(self, expression):
        lexer = Lexer(expression)
        parser = Parser(lexer)
        return parser.parse()

if __name__ == "__main__":
    interpreter = CalculatorInterpreter()

    while True:
        try:
            expression = input("Enter an arithmetic expression (or 'exit' to quit): ")
            if expression.lower() == 'exit':
                break

            result = interpreter.evaluate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
