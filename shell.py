from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter

input = input()
lexer = Lexer(input)
tokens = lexer.splitInput()
parser = Parser(tokens)
node = parser.expr()
interpreter = Interpreter(parser)
interpreter.visit_BinOp(node)
