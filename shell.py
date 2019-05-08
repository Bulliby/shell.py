from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
import os

input = input()
lexer = Lexer(input)
tokens = lexer.splitInput()
parser = Parser(tokens)
node = parser.expr()
interpreter = Interpreter(node)
interpreter.visit_BinOp(node)
