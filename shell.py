WORD, NAME, NEWLINE, IO_NUMBER, AND_IF, OR_IF, DLESS,  DGREAT,  LESSAND,  GREATAND  = 'WORD', 'NAME', 'NEWLINE', 'IO_NUMBER', 'AND_IF', 'OR_IF', 'DLESS',  'DGREAT',  'LESSAND',  'GREATAND'

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
        self.currentToken = Token(None);

    def advance(self):
        if (self.pos < len(self.text) - 1):
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def error(self):
        raise Exception ('Invalid Token')

    def get_next_token(self):
        while self.current_char:

            if self.current_char == '\n':
                self.advance()
                return self.currentToken
            
            else:
                self.currentToken.addChar(self.current_char)
                self.advance()

        return self.currentToken

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
        print(token.value)
        #interpreter = Interpreter(lexer)
        #result = interpreter.expr()
        #print(result)


if __name__ == '__main__':
    main()

