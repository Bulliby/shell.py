# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Redir.py                                                                  #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/11 18:32:24 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/30 14:05:57 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #
import os

class Redir():

    def __init__(self):
        self.pid = None

    def exec_redir(self, pipe, node):
        os.wait()
        os.close(pipe.w)
        os.dup2(pipe.r, 0)
        self.pid = pipe.pid
        self.write(self.open(node), 1)
        pipe.r, pipe.w = os.pipe()

    def write(self, fd, n):
        buf = os.read(0, n)
        while buf:
            os.write(fd, buf)
            buf = os.read(0, n)

    def open(self, node):
        if node.redir_type == 'GREAT':
            return os.open(node.file, os.O_TRUNC | os.O_CREAT | os.O_WRONLY)
        else:
            return os.open(node.file, os.O_CREAT | os.O_APPEND | os.O_WRONLY)

         
    def exec_only_redir(self, cmd, file):
        r, w = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            os.close(r)
            os.dup2(w, 1)
            os.execvp(cmd.cmd, cmd.suffix)
    
        #os.wait()
        os.close(w)
        os.dup2(r, 0)
        self.write(self.open(file), 1)
