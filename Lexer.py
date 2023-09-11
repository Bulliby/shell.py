# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Lexer.py                                                                  #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:55:28 by bulliby            \     \_\ \     /      #
#    Updated: 2022/06/30 17:43:59 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

class Token():
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return 'This object is a Token of the type {type}  with value {value}'.format(type=self.token, value=self.value)

class Lexer:
    def __init__(self, userInput):
        self.userInput = userInput
        self.pos = 0
        self.len = len(self.userInput)
        self.operators = {
            "OR"     : "||",
            "AND"    : "&&",
            "DLESS"     : "<<",
            "DGREAT"   :  ">>",
        } 
        self.oneCharOperators = {
            "PIPE"      : "|",
            "LESS"      : "<",
            "GREAT"     : ">",
        } 

    def __str__(self):
        return "This object transform the user input in Lexems"

    def currentChar(self):
        return self.userInput[self.pos]

    def advance(self):
        self.pos += 1

    def advanceTwice(self):
        self.pos += 2
        
    def error(self):
        raise Exception('Invalid Token')

    # For 2 chars operator
    def peekOneMoreChar(self):
        peek_pos = self.pos + 1
        if peek_pos > self.len - 1:
            return None
        else:
            return self.userInput[peek_pos]

    def handleWhiteSpace(self):
        while self.pos < self.len and self.currentChar().isspace():
            self.advance()

    def handleWord(self):
        result = ''
        while self.pos < self.len and self.currentChar().isascii()\
        and self.currentChar() != ' '\
        and self.currentChar() not in self.operators\
        and self.currentChar() not in self.oneCharOperators:
            result += self.currentChar()
            self.advance()

        return Token('WORD', result)

    def handle2CharOperator(self):
        for k, op in self.operators.items():
            if op[0] == self.currentChar():
                if op[1] == self.peekOneMoreChar():
                    return Token(k, op)
        return None

    def handleOperator(self):
        for k, op in self.oneCharOperators.items():
            if op[0] == self.currentChar():
                    return Token(k, op)
        return None

    def splitInput(self):
        tokens = []
        while self.pos < self.len:
            if self.currentChar().isspace():
                self.handleWhiteSpace()
            elif self.handle2CharOperator():
                tokens.append(self.handle2CharOperator())
                self.advanceTwice()
            elif self.handleOperator():
                tokens.append(self.handleOperator())
                self.advance()
            elif self.currentChar().isascii():
                tokens.append(self.handleWord())
            else:
                raise Exception("Invalid Character : " + self.currentChar())

        tokens.append(Token(None, 0))
        return tokens

