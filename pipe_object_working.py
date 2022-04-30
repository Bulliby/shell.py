# **************************************************************************** #
#                                                                              #
#                                                                              #
#    pipe3elem2.py                                                             #
#                                                         ________             #
#    By: waxer <wellsguillaume+at+gmail.com>             /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2022/04/24 20:49:26 by waxer              \     \_\ \     /      #
#    Updated: 2022/04/30 20:00:49 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()

    def pipe_start(self, cmd):
        pid = os.fork()
        if pid == 0:
            os.close(self.r)
            os.dup2(self.w, 1)
            os.execvp(cmd[0], cmd)
        os.waitpid(pid, 0)

    def pipe_inter(self, cmd):
        self.r2, self.w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.close(self.r2)
            os.dup2(self.r, 0)
            os.dup2(self.w2, 1)
            os.execvp(cmd[0], cmd)
        os.close(self.w)
        os.close(self.r)
        self.r = self.r2
        self.w = self.w2
        os.waitpid(pid, 0)

    def pipe_end(self, cmd):
        pid = os.fork()
        if pid == 0:
            os.close(self.w2)
            os.dup2(self.r2, 0)
            os.execvp(cmd[0], cmd)
        os.close(self.r2)
        os.close(self.w2)
        os.waitpid(pid, 0)

pipe = Pipe()
pipe.pipe_start(["echo", "Hello"]) 
pipe.pipe_inter(["wc", "-c"])
pipe.pipe_inter(["ls", "-la"])
pipe.pipe_inter(["head", "-n 1"])
pipe.pipe_end(["wc", "-l"])
