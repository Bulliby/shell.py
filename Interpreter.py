# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/08 17:51:54 by bulliby             \________/\/\_/       #
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
                os.close(self.pipe.w)
                os.dup2(self.pipe.r, 0)
                os.execvp(node.right.value, [node.right.value])
            self.pipe.exec_pipe(self.visit_BinOp(node.right))
            if self.root is node:
                os.close(self.pipe.w)
                os.dup2(self.pipe.r, 0)
                os.execvp(node.right.value, [node.right.value])

