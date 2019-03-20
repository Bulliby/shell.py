# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/03/10 15:11:56 by bulliby             \________/\/\_/       #
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
            if left :
                Pipe(left, True)
            Pipe(right, True)
        else:
            return node.value
