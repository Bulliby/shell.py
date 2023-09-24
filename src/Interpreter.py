# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Interpreter.py                                                            #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/03/02 19:56:05 by bulliby            \     \_\ \     /      #
#    Updated: 2022/05/01 18:41:02 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #
from Parser import Cmd
from Parser import File
from Parser import Eol
from Parser import PipeOp
from Parser import RedirOp
from Parser import Semi
from Parser import PipeSequence
from Parser import Boolean
from Pipe import Pipe
from SimpleCommand import SimpleCommand
from Redir import Redir
from HandleProcesses import HandleProcesses
import os

class Interpreter():

    def __init__(self):
        self.handleProcesses = HandleProcesses()
        self.pipe = Pipe(self.handleProcesses)
        self.redir = Redir(self.handleProcesses)
        self.cmd = SimpleCommand(self.handleProcesses)
        # To handle && and ||
        self.lastStatus = None

    def visit_BinOp(self, node):
        if type(node) is Eol:
            self.visit_BinOp(node.left)

        if type(node) is Cmd and node.lonely == False:
            return node

        # If we have only one command, we simply execute it
        if type(node) is Cmd and node.lonely == True:
            self.lastStatus = self.cmd.exec(node)

        if type(node) is File:
            return node

        if type(node) is Semi:
            for child in node.childs:
                self.visit_BinOp(child)

        if type(node) is Boolean:
            left = self.visit_BinOp(node.left)
            if node.operator == 'AND' and self.lastStatus == 0:
                right = self.visit_BinOp(node.right)
            if node.operator == 'OR' and self.lastStatus != 0:
                right = self.visit_BinOp(node.right)

        # to handle expression like ls -l > toto | ls -l | grep I > tata
        if type(node) is PipeSequence:
            for child in node.childs:
                self.pipe = Pipe(self.handleProcesses)
                self.visit_BinOp(child)

        if type(node) is PipeOp:
            left = self.visit_BinOp(node.left)
            right = self.visit_BinOp(node.right)
            if node.start:
                self.pipe.pipe_start(left)
            if node.next not in ['PIPE', 'GREAT']:
                self.lastStatus = self.pipe.pipe_end(right)
            else:
                self.pipe.pipe_inter(right)
            return left

        if type(node) is RedirOp:
            left = self.visit_BinOp(node.left)
            right = self.visit_BinOp(node.right)
            # If we were previously in a pipe
            if node.piped_before:
                self.redir.exec_piped_redir(self.pipe, node, right)
            else:
                self.lastStatus = self.redir.exec_redir(left, right, node)
            return left
