###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

(NAME, NEWLINE, IO_NUMBER, AND_IF, OR_IF, DLESS,  DGREAT,  LESSAND,  
        GREATAND, OPERATOR, PIPE) = ('NAME', 'NEWLINE', 'IO_NUMBER', 'AND_IF', 
'OR_IF', 'DLESS',  'DGREAT',  'LESSAND',  'GREATAND', 'OPERATOR', 'PIPE')


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self): #Define what is this
        return self.__str__()

class Lexer:
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

        self.operators = {
            "OR_IF"     : "||",
            "AND_IF"    : "&&",
            "DLESS"     : "<<",
            "GREATAND"  : "&>",
            "LESSAND"   : "<&",
        } 

        self.u_operator = {
            "PIPE"      : "|",
            "AND"       : "&",
            "LESS"      : "<",
            "GREAT"     : ">",
        } 

    def error(self):
        raise Exception ('Invalid Token')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        return Token(NAME, result.upper())

    def d_operator(self):
        for k, op in self.operators.items():
            if op[0] == self.current_char:
                if op[1] == self.peek():
                    return Token(k, op)
        return None

    def operator(self):
        for k, op in self.u_operator.items():
            if op[0] == self.current_char:
                    return Token(k, op)
        return None


    def get_next_token(self):
        while self.current_char:
            #STEP from : http://pubs.opengroup.org/onlinepubs/9699919799//utilities/V3_chap02.html#tag_18_03

            #1:: If current char is new line
            if self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, "\n") 

            #2:: If current char is part of a double operator
            elif self.d_operator():
                d_operator = self.d_operator()
                self.advance()
                self.advance()
                return d_operator

            elif self.operator():
                operator = self.operator()
                self.advance()
                return operator

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            self.error()

        return Token(EOF, None)

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
        while token:
            lexer.current_token = Token(None)
            token = lexer.get_next_token()
            if (token != None):
                #print('token')
                print(token.value)


if __name__ == '__main__':
    main()

