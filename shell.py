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
    #interpreter = Interpreter()
    # To print the tree from the root element
    # print(root)
    # break
    #interpreter.visit_BinOp(root)
    str = input('42sh > ')
    if str == '':
        break
