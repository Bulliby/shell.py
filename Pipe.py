# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Pipe.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2022/06/30 13:33:06 by bulliby            \     \_\ \     /      #
#    Updated: 2022/06/30 13:33:07 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()
        self.r2 = False 
        self.w2 = False

    def pipe_start(self, cmd):
        pid = os.fork()
        if pid == 0:
            os.close(self.r)
            os.dup2(self.w, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.waitpid(pid, 0)

    def pipe_inter(self, cmd):
        self.r2, self.w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.close(self.r2)
            os.dup2(self.r, 0)
            os.dup2(self.w2, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.close(self.w)
        os.close(self.r)
        self.r = self.r2
        self.w = self.w2
        os.waitpid(pid, 0)

    def pipe_end(self, cmd):
        if self.r2 != False:
            pid = os.fork()
            if pid == 0:
                os.close(self.w2)
                os.dup2(self.r2, 0)
                os.execvp(cmd.cmd, cmd.suffix)
            os.close(self.r2)
            os.close(self.w2)
        else:
            pid = os.fork()
            if pid == 0:
                os.close(self.w)
                os.dup2(self.r, 0)
                os.execvp(cmd.cmd, cmd.suffix)
            os.close(self.r)
            os.close(self.w)
        os.waitpid(pid, 0)

