# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Parser.py                                                                 #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 20:02:11 by bulliby            \     \_\ \     /      #
#    Updated: 2022/05/02 23:05:59 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #
class BinOp():
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        self.last = False

    def __str__(self):
        return "This is a BinOp with left value {0}, token {1}, right value {2}".format(self.left, self.token, self.right)

    def setLast(self):
        self.last = True
        
class UnaryOp():
    def __init__(self, operator, elem):
        self.elem = elem
        self.operator = operator

    def __str__(self):
        return "This is a UnaryOp with value {0}".format(self.elem)

class Cmd():
    def __init__(self, cmd):
        self.cmd = cmd 
        self.suffix = []
        # The first suffix is the name of the command
        self.suffix.append(cmd) 
        # Only used to determine the place of commande in pipeline
        self.pos = False 

    def __str__(self):
        return "This a LEAF with value : {0} and suffix {1} with place {2}".format(self.cmd, self.suffix, self.pos)

    def push_suffix(self, suffix):
        self.suffix.append(suffix)

class PipeOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "This is a Pipe with left value {0}, right value {1}".format(self.left, self.right)

class RedirOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right
            
    def __str__(self):
        return "This is a Redir with left value {0}, right value {1}".format(self.left, self.right)

class File():
    def __init__(self, file, redir_type):
        self.file = file 
        self.redir_type = redir_type
        self.pos = False

    def __str__(self):
        return "This a FILE with file : {0} and redir {1}".format(self.file, self.redir_type)

class Eol():
    def __str__(self):
        return "This is the last element of the Command Line"

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
            print("Parse Error, Got {0}, Expected {1}".format(token, value))
        else:
            self.getNextToken()

    def program(self):
        """
        program        : statements EOL
        """
        node = self.statements_list()

        node = BinOp(node, 'EOL', Eol())
        self.eat(self.getToken(), None)
        
        return node

    def statements_list(self):
        """
        statements_list     : statements
                            | statements SEMI
                            | statements SEMI statement_list
                            ;
        """
        node = self.statements()

        results = [node]
        
        while self.getToken().token == 'SEMI':
            self.eat(self.getToken(), 'SEMI')
            results.append(self.statements())
        
        return results

    def statements(self):
        """
        statements          | command
                            | statements pipe_sequence
                            | statements redir_sequence
                            ;
        """
        left = self.command()

        if self.getToken().token == 'PIPE':
            self.pipe_sequence(left)
        if self.getToken().token == 'GREAT':
            self.redir_sequence(left)

        return left

    def pipe_sequence(self, left):
        """
        pipe_sequence       | pipe_sequence
                            | pipe_sequence redir_sequence
                            | PIPE command
                            ;
        """
        self.eat(self.getToken(), 'PIPE')
        PipeOp(left, self.statements())

    def redir_sequence(self, left):
        """
        redir_sequence      | redir_sequence
                            | REDIR FILE
                            ;
        """
        self.eat(self.getToken(), 'GREAT')
        RedirOp(left, self.statements())

    def command(self):
        """
        command             | COMMAND
                            ;
        """
        comp_cmd = Cmd(self.getToken().value)
        self.eat(self.getToken(), 'WORD')

        return comp_cmd
