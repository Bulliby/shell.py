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

    def exec_redir(self, pipe, file):
        fd = self.open(file)
        """
        In redir sequence, like : ls -l > toto > tata
        toto is created but empty and only tata is populated 
        """
        if file.pos == 'last':
            os.close(pipe.w)
            self.write(pipe.r, fd, 1)
            os.close(pipe.r)

    def exec_only_redir(self, cmd, file):
        r, w = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            os.close(r)
            os.dup2(w, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.close(w)
        self.write(r, self.open(file), 1)
        os.close(r)
        os.waitpid(self.pid, 0)

    def write(self, fd, file, n):
        buf = os.read(fd, n)
        while buf:
            os.write(file, buf)
            buf = os.read(fd, n)

    def open(self, node):
        if node.redir_type == 'GREAT':
            return os.open(node.file, os.O_TRUNC | os.O_CREAT | os.O_WRONLY)
        else:
            return os.open(node.file, os.O_CREAT | os.O_APPEND | os.O_WRONLY)

