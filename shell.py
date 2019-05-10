from Lexer import Lexer
from Parser import Parser
from Parser import Cmd
from Interpreter import Interpreter
import os

input = input()
lexer = Lexer(input)
tokens = lexer.splitInput()
parser = Parser(tokens)
node = parser.expr()

if (type(node) is Cmd):
    os.execvp(node.value, [node.value])
else:
    interpreter = Interpreter(node)
    interpreter.visit_BinOp(node)
