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
interpreter = Interpreter()
"""
if type(node) is Cmd:
    os.execvp(node.cmd, node.suffix) #Only one CMD
elif node.token in ['GREAT', 'GREATAND', 'DGREAT'] and type(node.left) is Cmd: # Only a REDIR
    interpreter.redir.exec_only_redir(
            interpreter.visit_BinOp(node.left), 
            interpreter.visit_BinOp(node.right)
    )
else:
"""
interpreter.visit_BinOp(node)
