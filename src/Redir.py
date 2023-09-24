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

from WaitProcess import WaitProcess

class Redir(WaitProcess):

    def __init__(self):
        self.pid = None

    def exec_piped_redir(self, pipe, redirOp, file):
        fd = self.open(file)
        """
        (comment 1)
        In redir sequence, like : ls -l > toto > tata
        toto is created but empty and only tata is populated 
        For POSIX shell sh
        """
        if redirOp.next != 'GREAT':
            os.close(pipe.w)
            self.write(pipe.r, fd, 1)
            os.close(pipe.r)

    def exec_redir(self, cmd, file, redirOp):
        fd = self.open(file)
        # same reason that (comment 1)
        if redirOp.next != 'GREAT':
            r, w = os.pipe()
            self.pid = os.fork()
            if self.pid == 0:
                os.close(r)
                os.dup2(w, 1)
                os.execvp(cmd.cmd, cmd.suffix)
            os.close(w)
            self.write(r, self.open(file), 1)
            os.close(r)
            return self.waitProcess(self.pid)

    def write(self, fd, file, n):
        buf = os.read(fd, n)
        while buf:
            os.write(file, buf)
            buf = os.read(fd, n)

    def open(self, node):
        return os.open(node.file, os.O_TRUNC | os.O_CREAT | os.O_WRONLY, mode=0o664)
