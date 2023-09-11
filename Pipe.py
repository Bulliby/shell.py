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

"""
    FileDescriptor (fd) are given by the Kernel. The rule is that the kernel
    assign the next fd number available to the fd created : 
    -   if we have the following fd : 0,1,2 the next one will be 3
    -   if we have 0,1,2,4 it will fill the gap and the new one will have
        number 3...

    dup2(fd, fd2):
    close fd2 and duplicate fd so will be created with the fd2 number. 
"""

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()
        self.r2 = False 
        self.w2 = False

    def pipe_start(self, cmd):
        print("start")
        pid = os.fork()
        if pid == 0:
            os.close(self.r)
            # Close stdout and duplicate w. (w is now stdout)
            os.dup2(self.w, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.waitpid(pid, 0)

    def pipe_inter(self, cmd):
        print("inter")
        self.r2, self.w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.close(self.r2)
            # Close stdin and duplicate r. (r is now stdin)
            os.dup2(self.r, 0)
            os.dup2(self.w2, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.close(self.w)
        os.close(self.r)
        self.r = self.r2
        self.w = self.w2
        os.waitpid(pid, 0)

    def pipe_end(self, cmd):
        print("last")
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

