# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Parser.py                                                                 #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 20:02:11 by bulliby            \     \_\ \     /      #
#    Updated: 2019/03/07 16:09:35 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

class BinOp():
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        
class Cmd():
    def __init__(self, value):
        self.value = value 

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def __str__(self):
        return 'This object handle the parsing of the expression'

    def getToken(self):
        return self.tokens[self.pos]

    def getNextToken(self):
        self.pos+=1

    def eat(self, token, value):
        """ 
        The eat function permit to check that the token from the Lexer
        follow the given grammar
        """
        if token.token != value:
            raise Exception("Parse Error")
        self.getNextToken()

    def expr(self):
        """
        expr        : commands (AND | OR commands)*
        """
        node = self.commands()
        while self.getToken().token in ['AND', 'OR']:
            if self.getToken().token == 'AND':
                token = self.getToken().token
                self.eat(self.getToken(), 'AND')
            elif self.getToken().token == 'OR':
                token = self.getToken().token
                self.eat(self.getToken(), 'OR')
            node = BinOp(node, token, self.commands())
        return node

    def commands(self):
        """
        commands    : CMD ((PIPE CMD)* | (REDIR FILE)*)*
        """
        cmd = Cmd(self.getToken().value)
        self.eat(self.getToken(), 'CMD')
        while self.getToken().token in ['PIPE']:
            operator = self.getToken().token
            self.eat(self.getToken(), 'PIPE')
            cmd2 = Cmd(self.getToken().value)
            self.eat(self.getToken(), 'CMD')
            cmd = BinOp(cmd, operator, cmd2)
        return cmd
