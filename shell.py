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
                #print('NL')
                self.current_token.type = NEWLINE
                self.advance()
                return self.current_token

            #2:: If current char is part of an operator
            elif self.current_token.type == OPERATOR and self.if_op_continuation():
                #print('continuation')
                self.current_token.addChar(self.current_char)

            #3:: If current char is the end of an operator
            elif self.current_token.type == OPERATOR and self.if_op_continuation() == 0:
                #print(self.current_token.value)
                #print('break')
                self.advance()
                return self.current_token

            #6:: Current char is a new operator
            if self.if_new_op():
                #print('new op')
                if self.current_token.type != None:
                    token_cp = copy.deepcopy(self.current_token)
                    self.current_token = Token(None)
                    self.current_token.type = OPERATOR
                    self.current_token.addChar(self.current_char)
                    self.advance()
                    return token_cp
                else:
                    self.current_token.type = OPERATOR
                    self.current_token.addChar(self.current_char)
            
            #7:: If blank
            elif self.current_char.isspace():
                #print('blank')
                self.whitespace()
                return self.current_token
            
            #8:: Word continuation
            elif self.current_token.type == WORD:
                #print('word continuation')
                self.current_token.addChar(self.current_char)

            #9:: New WORD
            else:
                #print('word')
                self.current_token.type == WORD
                self.current_token.addChar(self.current_char)

            self.advance()
        return None

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.result = 0

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.lexer.error()

    def programm(self):
        self.result = self.linebreak()
        

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
        if (token != None):
            #print('first token')
            print(token.value)
        while token:
            lexer.current_token = Token(None)
            token = lexer.get_next_token()
            if (token != None):
                #print('token')
                print(token.value)


if __name__ == '__main__':
    main()

