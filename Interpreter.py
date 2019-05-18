# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/18 15:28:01 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Parser import Cmd
from Pipe import Pipe
from Redir import Redir
import os

class Interpreter():

    def __init__(self, root):
        self.root = root
        self.pipe = Pipe()
        self.redir = Redir()


    def visit_BinOp(self, node):
        if type(node) is Cmd:
            return node
        else:
            if node.token == 'PIPE':
                self.pipe.exec_pipe(self.visit_BinOp(node.left))
                if self.root is node:
                    self.pipe.exec_last_pipe(node) 
                self.pipe.exec_pipe(self.visit_BinOp(node.right))

            if node.token in ['GREAT', 'GREATAND', 'DGREAT']:
                self.visit_BinOp(node.left)
                self.redir.exec_redir(self.pipe, self.visit_BinOp(node.right))
