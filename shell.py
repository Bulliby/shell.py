"""Shell Lexer/Parse in python"""

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

(NAME, NEWLINE, IO_NUMBER, AND_IF, OR_IF, DLESS,  DGREAT,  LESSAND,  
        GREATAND, OPERATOR, PIPE, EOF) = ('NAME', 'NEWLINE', 'IO_NUMBER', 'AND_IF', 
'OR_IF', 'DLESS',  'DGREAT',  'LESSAND',  'GREATAND', 'OPERATOR', 'PIPE', 'EOF')


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
                return Token(NEWLINE, '\n') 

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


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class NoOp(AST):
    pass

class NewLine(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """program  : linebreak complete_commands linebreak
                    | linebreak
                    ;      
        """
        self.linebreak() 
        node = self.complete_commands()
        self.linebreak()
        return node

    def linebreak(self):
        """ linebreak   : newline_list
                        | /* empty */
                        ;
        """
        return self.newline_list()


    def newline_list(self):
        """ newline_list    : NEWLINE
                            | newline_list NEWLINE
                            ;
        """
        token = self.current_token
        node = None
        while self.current_token.type == NEWLINE:
            node = NewLine(self.current_token)
            self.eat(NEWLINE)

        return node
            

    def complete_commands(self):
        """ complete_commands: complete_commands newline_list and_or
                             | and_or
                             ;
        """
        print("complete_commands")
        """
        if self.current_token.type == PIPE:
            self.eat(PIPE)
        while self.current_token.type == PIPE:
            sel
        """

    def and_or(self):
        """ and_or  : pipe_sequence
                    | and_or AND_IF linebreak pipe_sequence
                    | and_or OR_IF  linebreak pipe_sequence
                    ;
        """ 
        print("and_or")

    def pipe_sequence(self):
        """ pipe_sequence : command
                          | pipe_sequence '|' linebreak command
                          ;
        """

    def simple_command(self):
        """ simple_command   : cmd_prefix cmd_word cmd_suffix
                             | cmd_prefix cmd_word
                             | cmd_prefix
                             | cmd_name cmd_suffix
                             | cmd_name
        """ 

    def empty(self):
        return NoOp()

def main():
    while true:
        try:
            text = input('lexer> ')
        except eoferror:
            break
        if not text:
            continue
        lexer = lexer(text)
        token = lexer.get_next_token()
        while token:
            lexer.current_token = Token(None)
            token = lexer.get_next_token()
            if (token != None):
                #print('token')
                print(token.value)


if __name__ == '__main__':
    main()

