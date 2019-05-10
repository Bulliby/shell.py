# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/10 22:43:53 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Parser import Cmd
from Pipe import Pipe
import os

class Interpreter():

    def __init__(self, root):
        self.root = root
        self.pipe = Pipe()

    def visit_BinOp(self, node):
        if type(node) is Cmd:
            return node.value
        else:
            self.pipe.exec_pipe(self.visit_BinOp(node.left))
            if self.root is node:
                self.pipe.exec_last_pipe(node) 
            self.pipe.exec_pipe(self.visit_BinOp(node.right))
