# **************************************************************************** #
#                                                                              #
#                                                                              #
#    shell.py                                                                  #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2023/09/29 13:09:30 by bulliby            \     \_\ \     /      #
#    Updated: 2023/09/29 13:09:33 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

from Lexer import Lexer
from Parser import Parser
from Parser import Cmd
from Interpreter import Interpreter
import os
import readline

str = input('42sh > ')
while True:
    lexer = Lexer(str)
    tokens = lexer.splitInput()
    parser = Parser(tokens)
    root = parser.program()
    interpreter = Interpreter()
    # To print the tree from the root element
    # break
    #print(root)
    interpreter.visit_BinOp(root)
    str = input('42sh > ')
    if str == '':
        break
