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
    def __init__(self, left, right, nextNode):
        self.left = left
        self.right = right

        if type(self.left) is Cmd:
            self.left.pos = 'start'
        if nextNode.token == 'PIPE' or nextNode.token == 'GREAT':
            self.right.pos = 'inter'
        else:
            self.right.pos = 'last'

    def __str__(self):
        return "This is a Pipe with left value {0}, right value {1}".format(self.left, self.right)

class RedirOp():
    def __init__(self, left, right, nextNode):
        self.left = left
        self.right = right

        if type(self.left) is Cmd:
            self.left.pos = 'start'
        if nextNode.token == 'GREAT':
            self.right.pos = 'inter'
        else:
            self.right.pos = 'last'
            
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
            raise Exception("Parse Error, Got {0}, Expected {1}".format(token, value))
        self.getNextToken()

    def expr(self):
        """
        expr        : commands (AND | OR commands)* EOL
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
        
        node = BinOp(node, 'EOL', Eol())
        self.eat(self.getToken(), None)
        
        return node

    def commands(self):
        """
        commands    : comp_cmd ((PIPE comp_cmd)* | (GREAT file)*)
        """
        commands = self.comp_cmd()
                
        while self.getToken().token in ['PIPE']:
            self.eat(self.getToken(), 'PIPE')
            comp_cmd_right = self.comp_cmd()
            commands = PipeOp(commands, comp_cmd_right, self.getToken())

        while self.getToken().token in ['GREAT']:
            operator = self.getToken().token
            self.eat(self.getToken(), 'GREAT')
            file = File(self.getToken().value, operator)
            self.eat(self.getToken(), 'WORD')
            commands = RedirOp(commands, file, self.getToken())

        return commands

    def comp_cmd(self):
        """
        comp_cmd    : cmd (cmd_suffix)*
        """
        comp_cmd = Cmd(self.getToken().value)
        self.eat(self.getToken(), 'WORD')

        while self.getToken().token == 'WORD':
            comp_cmd.push_suffix(self.getToken().value)
            self.eat(self.getToken(), 'WORD')

        return comp_cmd
