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
        os.close(pipe.w)
        self.write(pipe.r, self.open(file), 1)
        os.close(pipe.r)

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

