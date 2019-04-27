from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
import os

input = input()
lexer = Lexer(input)
tokens = lexer.splitInput()
parser = Parser(tokens)
node = parser.expr()
interpreter = Interpreter(parser)
last = interpreter.visit_BinOp(node)
pid = os.fork()
if pid == 0:
    os.close(last.w)
    os.dup2(last.r, 0)
    os.execvp('wc' , ['wc'])
