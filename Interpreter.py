# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2022/05/01 18:41:02 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #
from Parser import Cmd
from Parser import File
from Parser import Eol
from Parser import PipeTest
from Parser import RedirTest
from Pipe import Pipe
from Exec import Exec
from Redir import Redir
from Boolean import Boolean
from IPCChain import IPCChain
import os

class Interpreter():

    def __init__(self):
        self.pipe = Pipe()
        self.chain = IPCChain()
        self.redir = Redir()
        self.boolean = Boolean()
        self.cmd = Exec()

    def visit_BinOp(self, node):
        if type(node) is Cmd or type(node) is File or type(node) is Eol:
            return node
        else:
            if type(node) is PipeTest:
                # Si on commence la chaine pipes
                left = self.visit_BinOp(node.left)
                if node.pos == 'start':
                    self.chain.start_chain(left)
                right = self.visit_BinOp(node.right)
                if node.pos == 'inter':
                    self.chain.pipe_inter(right)
                else:
                    self.chain.pipe_end(right)
                #print('pipe')

            elif node.token in ['GREAT', 'GREATAND', 'DGREAT']:
                if type(node.left) is Cmd and type(node.right) is File:
                    self.visit_BinOp(node.left)
                    self.redir.exec_only_redir(node.left, node.right)
                else:
                    self.visit_BinOp(node.left)
                    self.redir.exec_redir(self.pipe, self.visit_BinOp(node.right))
                #print('redir')

            elif node.token in ['OR', 'AND']:
                self.visit_BinOp(node.left)
                if type(node.left) is Cmd:
                    self.cmd.exec_cmd(node.left)
                    ret = self.boolean.checkStatus(self.cmd.pid) 
                elif node.left.token in ['GREAT', 'GREATAND', 'DGREAT']:
                    ret = self.boolean.checkStatus(self.redir.pid) 
                else:
                    self.pipe.sequence_end()
                    ret = self.boolean.checkStatus(self.pipe.pid) 
                if (ret == 0 and node.token == 'OR') or (ret != 0 and node.token == 'AND'):
                    return
                self.visit_BinOp(node.right)
                if type(node.right) is  Cmd:
                    self.cmd.exec_cmd(node.right)
                #print('and')

            elif node.token == 'EOL':
                self.visit_BinOp(node.left)
                self.visit_BinOp(node.right)
                if type(node.left) is Cmd:
                    self.cmd.exec_cmd(node.left)
                elif type(node.left) is PipeTest:
                    pass
                elif type(node.left) is RedirTest:
                    pass
                #print('eol')
