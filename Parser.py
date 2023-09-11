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
        self.suffix.append(cmd) # The first suffix is the name of the command
        self.pipePlace = False # Only used to determine the place of commande in pipeline

    def __str__(self):
        return "This a LEAF with value : {0} and suffix {1} with place {2}".format(self.cmd, self.suffix, self.pipePlace)

    def push_suffix(self, suffix):
        self.suffix.append(suffix)

class File():
    def __init__(self, file, redir_type):
        self.file = file 
        self.redir_type = redir_type

    def __str__(self):
        return "This a LEAF with file : {0} and redir {1}".format(self.file, self.redir_type)

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
            raise Exception("Parse Error")
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
        commands    : comp_cmd ((PIPE comp_cmd)* | (GREAT file))
        """
        commands = self.comp_cmd()

        while self.getToken().token in ['PIPE']:
            commands.pipePlace = 'start'
            pipe_count = 1
            operator = self.getToken().token
            self.eat(self.getToken(), 'PIPE')
            comp_cmd_right = self.comp_cmd()
            if (pipe_count > 0 and self.getToken().token == 'PIPE' or self.getToken().token == 'GREAT'):
                place = 'inter'
            else:
                place = 'last'
            comp_cmd_right.pipePlace = place
            pipe_count+=1
            commands = BinOp(commands, operator, comp_cmd_right)
                
        if self.getToken().token == 'GREAT':
            operator = self.getToken().token
            if operator == 'GREAT':
                self.eat(self.getToken(), 'GREAT')
            file = File(self.getToken().value, operator)
            self.eat(self.getToken(), 'WORD')
            commands = BinOp(commands, operator, file)

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
