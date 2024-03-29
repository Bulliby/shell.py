"""
Permit to read my parser output and print it in a png, really useful to see 
if your AST tree looks correct

python generateAstDot.py command_sample > ast.dot && dot -Tpng -o ast.png ast.dot
"""
import argparse
import textwrap

from src.Lexer import Lexer
from src.Parser import Parser

from src.Parser import PipeOp
from src.Parser import RedirOp
from src.Parser import Cmd
from src.Parser import Semi
from src.Parser import PipeSequence
from src.Parser import Eol
from src.Parser import File
from src.Parser import Boolean

class ASTVisualizer():
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=circle, fontsize=12, fontname="Courier", height=.1];
          ranksep=.3;
          edge [arrowsize=.5]

        """)]
        self.dot_body = []
        self.dot_footer = ['}']


    def visit_BinOp(self, node):
        if type(node) is Cmd:
            s = '  node{} [label="{}"]\n'.format(self.ncount, node.cmd) 
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1

        if type(node) is File:
            s = '  node{} [label="{}"]\n'.format(self.ncount, node.file) 
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1

        if type(node) is Semi:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "semi")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            for child in node.childs:
                self.visit_BinOp(child)
                s = '  node{} -> node{}\n'.format(node._num, child._num)
                self.dot_body.append(s)

        if type(node) is Boolean:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "bool")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            self.visit_BinOp(node.left)
            s = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.dot_body.append(s)
            self.visit_BinOp(node.right)
            s = '  node{} -> node{}\n'.format(node._num, node.right._num)
            self.dot_body.append(s)

        if type(node) is PipeSequence:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "pipes")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            for child in node.childs:
                self.visit_BinOp(child)
                s = '  node{} -> node{}\n'.format(node._num, child._num)
                self.dot_body.append(s)

        if type(node) is PipeOp:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "pipe")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            self.visit_BinOp(node.left)
            s = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.dot_body.append(s)
            self.visit_BinOp(node.right)
            s = '  node{} -> node{}\n'.format(node._num, node.right._num)
            self.dot_body.append(s)

        if type(node) is RedirOp:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "redir")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            self.visit_BinOp(node.left)
            s = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.dot_body.append(s)
            self.visit_BinOp(node.right)
            s = '  node{} -> node{}\n'.format(node._num, node.right._num)
            self.dot_body.append(s)

        if type(node) is Eol:
            s = '  node{} [label="{}"]\n'.format(self.ncount, "eol")
            self.dot_body.append(s)
            node._num = self.ncount
            self.ncount += 1
            left = self.visit_BinOp(node.left)
            s = '  node{} -> node{}\n'.format(node._num, node.left._num)
            self.dot_body.append(s)

    def gendot(self):
        tree = self.parser.program()
        self.visit_BinOp(tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)


def main():
    argparser = argparse.ArgumentParser(
        description='Generate an AST DOT file.'
    )
    argparser.add_argument(
        'fname',
        help='Shell.py visualizer'
    )
    args = argparser.parse_args()
    fname = args.fname
    text = open(fname, 'r').read()

    lexer = Lexer(text)
    tokens = lexer.splitInput()
    parser = Parser(tokens)
    viz = ASTVisualizer(parser)
    content = viz.gendot()
    print(content)


if __name__ == '__main__':
    main()
