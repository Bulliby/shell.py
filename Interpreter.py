# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2019/03/07 13:10:27 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Parser import Cmd

class Interpreter():

    def __init__(self, root):
        self.root = root

    def visit_BinOp(self, node):
        if type(node) is not Cmd:
            left = self.visit_BinOp(node.left)
            right = self.visit_BinOp(node.right)
            return left + right
        else:
            return node.value
