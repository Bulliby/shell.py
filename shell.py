WORD, NAME, NEWLINE, IO_NUMBER, AND_IF, OR_IF, DLESS,  DGREAT,  LESSAND,  GREATAND  = 'WORD', 'NAME', 'NEWLINE', 'IO_NUMBER', 'AND_IF', 'OR_IF', 'DLESS',  'DGREAT',  'LESSAND',  'GREATAND'
import copy

class Token:
    def __init__(self, type):
        self.type = type
        self.value = ''

    def addChar(self, value):
        self.value += value;

class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]
        self.current_token = Token(None)
        self.operators = [
                '||',
                '&&',
                '<<',
                '&>',
                '<&',
                ]

    def advance(self):
        if (self.pos < len(self.text) - 1):
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def error(self):
        raise Exception ('Invalid Token')

    def if_new_op(self):
        for op in self.operators:
            if op[0] == self.current_char:
                return 1
        return 0

    def if_op_continuation(self):
        for op in self.operators:
            if op.startswith(self.current_token.value + self.current_char):
                return 1
        return 0


    def get_next_token(self):
        while self.current_char:

            # If current char is part of an operator
            if len(self.current_token.value) > 0 and self.if_op_continuation():
                self.current_token.addChar(self.current_char)

            # If current char is the end of an operator
            elif len(self.current_token.value) > 0 and self.if_op_continuation() == 0:
                print('break')
                self.advance()
                return self.current_token
            
            # If current char is part of the first operator
            elif self.pos == 0 and self.if_new_op():
                self.current_token = Token(None)
                self.current_token.addChar(self.current_char)

            # If current char is the start of new operator
            elif self.if_new_op():
                token_cp = copy.deepcopy(self.current_token)
                self.current_token = Token(None)
                self.current_token.addChar(self.current_char)
                self.advance()
                return token_cp

            self.advance()
        return None

def main():
    while True:
        try:
            text = input('lexer> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        token = lexer.get_next_token()
        while token:
            token = lexer.get_next_token()


if __name__ == '__main__':
    main()

