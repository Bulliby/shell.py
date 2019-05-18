# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Redir.py                                                                  #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/11 18:32:24 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/12 15:03:01 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #


import os

class Redir():

    def exec_redir(self, pipe, file):
        os.wait()
        os.close(pipe.w)
        os.dup2(pipe.r, 0)
        fd = os.open(file, os.O_RDWR)
        buf = os.read(0, 1)
        while buf:
            os.write(fd, buf)
            buf = os.read(0, 1)
         
    def exec_only_redir(self, cmd, file):
            r, w = os.pipe()
            pid = os.fork()
            if pid == 0:
                os.close(r)
                os.dup2(w, 1)
                os.execvp(cmd, [cmd])
        
            os.wait()
            os.close(w)
            os.dup2(r, 0)
            fd = os.open(file, os.O_RDWR)
            buf = os.read(0, 1000)
            while buf:
                os.write(fd, buf)
                buf = os.read(0, 1000)
