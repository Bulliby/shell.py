# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Pipe.py                                                                   #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/11 18:32:52 by bulliby            \     \_\ \     /      #
#    Updated: 2022/05/01 18:46:43 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #
# import os
# from Parser import Cmd

# class Pipe():

#     def __init__(self):
#         self.r, self.w = os.pipe()
#         self.pid = None


#     def exec_pipe(self, cmd):
#         if type(cmd) is Cmd:
#             r2, w2 = os.pipe()
#             self.pid = os.fork()
#             if self.pid == 0:
#                 os.close(self.w)
#                 os.dup2(self.r, 0)
#                 os.close(r2)
#                 os.dup2(w2, 1)
#                 os.execvp(cmd.cmd, cmd.suffix)
              
#             os.close(self.w)
#             os.close(self.r)
#             self.r = r2
#             self.w = w2

#     def sequence_end(self):
#         os.close(self.w)
#         os.dup2(self.r, 0)
#         buf = os.read(0, 1)
#         os.write(1, buf)
#         while buf:
#             buf = os.read(0, 1)
#             os.write(1, buf)
#         os.close(self.r)
#         self.r, self.w = os.pipe()

#     def last(self):
#         os.close(self.w)
#         os.dup2(self.r, 0)
#         buf = os.read(0, 1)
#         os.write(1, buf)
#         while buf:
#             buf = os.read(0, 1)
#             os.write(1, buf)

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

