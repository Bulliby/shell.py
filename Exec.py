# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Exec.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/30 12:54:58 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/30 13:03:57 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

"""
This class permit the execution of simple command. With no pipe or redir.
"""

class Exec():
    def __init__(self):
        self.pid = None

    def exec_cmd(self, node):
        self.pid = os.fork()
        if self.pid == 0:
            os.execvp(node.cmd, node.suffix)
