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
class Semi():
    def __init__(self, child):
        self.childs = [child]

    def __str__(self):
        ret = ";SEMILICON compound statements containing :"
        count = 0
        for child in self.childs:
            ret += "For index {0}: {1}".format(count, child)
            count+=1
        return ret
        
class Cmd():
    def __init__(self, cmd):
        self.cmd = cmd 
        self.suffix = []
        # The first suffix is the name of the command
        self.suffix.append(cmd) 
        # Used to identify a simple command like ls
        self.lonely = False

    def __str__(self):
        return ";COMMAND with value : {0} and suffix {1} with place {2}".format(self.cmd, self.suffix, self.pos)

    def push_suffix(self, suffix):
        self.suffix.append(suffix)

    def setLonely(self):
        self.lonely = True

class PipeOp():
    def __init__(self, left, right, nnext, start):
        self.left = left
        self.right = right
        self.next = nnext
        # We do a special case for the starting pipe sequence
        # and for end. It's related of how os.pipe works
        self.start = start
        self.last = False

    def setLast(self):
        self.last = True

    def __str__(self):
        return ";Pipe with left value {0}, right value {1} and next {2} start info {3} last info {4}".format(self.left, self.right, self.next, self.start, self.last)

class PipeSequence():
    def __init__(self, child):
        self.childs = [child]

    def __str__(self):
        ret = "; PipeSequence containing :"
        count = 0
        for child in self.childs:
            ret += "For index {0}: {1}".format(count, child)
            count+=1
        return ret

class RedirOp():
    def __init__(self, left, right, nnext, piped_before):
        self.left = left
        self.right = right
        self.next = nnext
        # This a special case who handle the redirecting output form a pipe sequence
        self.piped_before = piped_before
            
    def __str__(self):
        return ";Redir with left value {0}, right value {1} and next {2}".format(self.left, self.right, self.next)

class File():
    def __init__(self, file, redir_type):
        self.file = file 
        self.redir_type = redir_type
        self.pos = False

    def __str__(self):
        return "This a FILE with file : {0} and redir {1}".format(self.file, self.redir_type)

class Eol():
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return ";Eol with left value {0}, token {1}, right value {2}".format(self.left, self.token, self.right)

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
        nodes = self.statements_list()

        node = Eol(nodes, 'EOL', None)
        self.eat(self.getToken(), None)
        
        return node

    def statements_list(self):
        node = self.pipes_list()

        semilicon = Semi(node)
        
        while self.getToken().token == 'SEMI':
            self.eat(self.getToken(), 'SEMI')
            semilicon.childs.append(self.pipes_list())
        
        return semilicon

    def pipes_list(self):
        node = self.statements()

        pipes = PipeSequence(node)
        
        while self.getToken().token == 'PIPE':
            self.eat(self.getToken(), 'PIPE')
            pipes.childs.append(self.statements())
        
        return pipes

    def statements(self):
        """
        statements : 
        """
        node = self.pipe_sequence()

        piped_before =  type(node) is PipeOp

        while self.getToken().token == 'GREAT':
            operator = self.getToken().token
            self.eat(self.getToken(), 'GREAT')
            node = RedirOp(node, self.file(operator), self.getToken().token, piped_before)

        if type(node) is Cmd:
            node.setLonely()

        return node

    def pipe_sequence(self):
        """
        pipe_sequence : command (PIPE command)*
        """
        node = self.command()
        count = 0

        while self.getToken().token == 'PIPE':
            self.eat(self.getToken(), 'PIPE')
            node = PipeOp(node, self.command(), self.getToken().token, count == 0)
            count+=1

        return node

    def file(self, operator):
        file = File(self.getToken().value, operator)
        self.eat(self.getToken(), 'WORD')
        return file

    def command(self):
        """
        command             | COMMAND
                            ;
        """
        comp_cmd = Cmd(self.getToken().value)
        self.eat(self.getToken(), 'WORD')

        while self.getToken().token == 'WORD':
            comp_cmd.push_suffix(self.getToken().value)
            self.eat(self.getToken(), 'WORD')

        return comp_cmd
