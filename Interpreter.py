# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/03/08 15:57:23 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Parser import Cmd
from Pipe import Pipe

class Interpreter():

    def __init__(self, root):
        self.root = root
        self.count = 0

    def visit_BinOp(self, node):
        if type(node) is not Cmd:
            left = self.visit_BinOp(node.left)
            right = self.visit_BinOp(node.right)
            self.count = self.count + 1 
            if left :
                Pipe(left, self.count % 2 == 0)
                self.count = self.count + 1 
            Pipe(right, self.count % 2 == 0)
        else:
            return node.value
