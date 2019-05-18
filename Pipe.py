# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Pipe.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/11 18:32:52 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/18 13:33:47 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

from Parser import Cmd

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()



    def exec_pipe(self, cmd):
        if type(cmd) is Cmd:
            r2, w2 = os.pipe()
            pid = os.fork()
            if pid == 0:
                os.close(self.w)
                os.dup2(self.r, 0)
                os.close(r2)
                os.dup2(w2, 1)
                os.execvp(cmd.cmd, cmd.suffix)
               
            os.close(self.w)
            os.close(self.r)
            self.r = r2
            self.w = w2


    def exec_last_pipe(self, node):
        os.close(self.w)
        os.dup2(self.r, 0)
        os.execvp(node.right.cmd, node.right.suffix)
