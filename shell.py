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
    node = parser.expr()
    interpreter = Interpreter()
    interpreter.visit_BinOp(node)
    str = input('42sh > ')
    if str == '':
        break
