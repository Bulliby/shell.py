# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Exec.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/30 12:54:58 by bulliby            \     \_\ \     /      #
#    Updated: 2022/06/30 13:33:29 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

from WaitProcess import WaitProcess

"""
This class permit the execution of simple command. With no pipe or redir.
"""

class SimpleCommand(WaitProcess):

    def exec(self, node):
        pid = os.fork()
        if pid == 0:
            os.execvp(node.cmd, node.suffix)
        return self.waitProcess(pid)
