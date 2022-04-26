# **************************************************************************** #
#                                                                              #
#                                                                              #
#    pipe3elem.py                                                              #
#                                                         ________             #
#    By: waxer <wellsguillaume+at+gmail.com>             /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2022/04/24 20:44:44 by waxer              \     \_\ \     /      #
#    Updated: 2022/04/26 16:28:53 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os
import signal
import sys

def exex_command(cmd1, cmd2, cmd3):
    r, w  = os.pipe() 
    r2,  w2 = os.pipe() 
    stdin  = sys.stdin.fileno() # usually 0
    stdout = sys.stdout.fileno() # usually 1
    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.close(r2)
        os.close(w2)
        os.dup2(w, stdout)
        os.execvp(cmd1[0], cmd1)
    os.waitpid(pid, 0)

    pid = os.fork()
    if pid == 0:
        os.close(w)
        os.close(r2)
        os.dup2(r, stdin)
        os.dup2(w2, stdout)
        os.execvp(cmd2[0], cmd2)
    os.close(w)
    os.waitpid(pid, 0)

    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.close(w2)
        os.dup2(r2, stdin)
        os.execvp(cmd3[0], cmd3)
    os.close(r)
    os.close(w2)
    os.close(r2)
    os.waitpid(pid, 0)
    

def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                    -1,          # Wait for any child process
                    )
        except OSError:
            return

        if pid == 0:  # no more zombies
            return

exex_command(["echo", "Hello"], ["wc", "-c"], ["wc", "-c"])
