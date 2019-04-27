# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/04/30 22:04:42 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Parser import Cmd
from Pipe import Pipe

class Interpreter():

    def __init__(self, root):
        self.pipe = None

    def visit_BinOp(self, node):
        if type(node) is not Cmd:
            left = self.visit_BinOp(node.left)
            right = self.visit_BinOp(node.right)
            #print('right =>', right)
            #print('left =>', left)
            return right
        else:
            self.pipe = Pipe(node.value, self.pipe).exec_pipe()
            return self.pipe
