# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Parser.py                                                                 #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 20:02:11 by bulliby            \     \_\ \     /      #
#    Updated: 2019/03/08 15:57:45 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

class BinOp():
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return "This is a BinOp with left value {0} and right value {1}".format(self.left, self.right)
        
class Cmd():
    def __init__(self, value):
        self.value = value 

    def __str__(self):
        return "This a LEAF with value : {0}".format(self.value)

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
        while self.getToken().token in ['GREAT', 'GREATAND', 'DGREAT']:
            operator = self.getToken().token
            if operator == 'GREAT':
                self.eat(self.getToken(), 'GREAT')
                file = Cmd(self.getToken().value)
            if operator == 'GREATAND':
                self.eat(self.getToken(), 'GREATAND')
                file = Cmd(self.getToken().value)
            if operator == 'DGREAT':
                self.eat(self.getToken(), 'DGREAT')
                file = Cmd(self.getToken().value)
            self.eat(self.getToken(), 'CMD')
            cmd = BinOp(cmd, operator, file)
        return cmd
