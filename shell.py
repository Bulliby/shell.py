WORD, NAME, NEWLINE, IO_NUMBER, AND_IF, OR_IF, DLESS,  DGREAT,  LESSAND,  GREATAND, OPERATOR = 'WORD', 'NAME', 'NEWLINE', 'IO_NUMBER', 'AND_IF', 'OR_IF', 'DLESS',  'DGREAT',  'LESSAND',  'GREATAND', 'OPERATOR'
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

    def whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char:
            #STEP from : http://pubs.opengroup.org/onlinepubs/9699919799//utilities/V3_chap02.html#tag_18_03

            #1:: If current char is new line
            if (self.current_char == '\n'):
                self.advance()
                return self.current_token

            #2:: If current char is part of an operator
            elif len(self.current_token.value) > 0 and self.if_op_continuation():
                print('continuation')
                self.current_token.addChar(self.current_char)

            #3:: If current char is the end of an operator
            elif len(self.current_token.value) > 0 and self.if_op_continuation() == 0:
                print('break')
                self.advance()
                return self.current_token
            
            #6:: If current char is part of the first operator
            elif self.pos == 0 and self.if_new_op():
                print('new_op_first')
                self.current_token.addChar(self.current_char)

            #6:: If current char is the start of new operator
            elif self.if_new_op():
                print('new_op')
                self.current_token.addChar(self.current_char)
                self.advance()
                return self.current_token

            #7:: If blank
            elif self.current_char.isspace():
                self.whitespace()
                return self.current_token

            #8:: If part of a WORD
            elif len(self.current_token.value) > 0 and self.current_char.isalnum():
                self.current_token.addChar(self.current_char)

            #9:: Append char to WORD
            else:
                self.current_token.addChar(self.current_char)
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
            print(lexer.current_token.value)
            lexer.current_token = Token(None)
            token = lexer.get_next_token()


if __name__ == '__main__':
    main()

