# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Pipe.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/11 18:32:52 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/12 11:40:13 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()
        self.pid = None

    def exec_pipe(self, cmd):
        if type(cmd) is str:
            r2, w2 = os.pipe()
            self.pid = os.fork()
            if self.pid == 0:
                os.close(self.w)
                os.dup2(self.r, 0)
                os.close(r2)
                os.dup2(w2, 1)
                os.execvp(cmd, [cmd])
            
            os.close(self.w)
            os.close(self.r)
            self.r = r2
            self.w = w2

    def exec_last_pipe(self, node):
        os.close(self.w)
        os.dup2(self.r, 0)
        os.execvp(node.right.value, [node.right.value])
