from Lexer import Lexer
from Parser import Parser
from Parser import Cmd
from Interpreter import Interpreter
import os

str = input()
while True:
    lexer = Lexer(str)
    tokens = lexer.splitInput()
    parser = Parser(tokens)
    node = parser.expr()
    interpreter = Interpreter()
    interpreter.visit_BinOp(node)
    str = input()
    if str == '':
        break
