# **************************************************************************** #
#                                                                              #
#                                                                              #
#    pipe3elem.py                                                              #
#                                                         ________             #
#    By: waxer <wellsguillaume+at+gmail.com>             /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2022/04/24 20:44:44 by waxer              \     \_\ \     /      #
#    Updated: 2022/04/26 21:15:42 by waxer               \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os
import signal
import sys

def exex_command(cmd1, cmd2, cmd3, cmd4):
    r, w  = os.pipe() 
    stdin  = sys.stdin.fileno()
    stdout = sys.stdout.fileno()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.dup2(w, stdout)
        os.execvp(cmd1[0], cmd1)
    os.waitpid(pid, 0)

    r2,  w2 = os.pipe() 
    pid = os.fork()
    if pid == 0:
        os.close(w)
        os.close(r2)
        os.dup2(r, stdin)
        os.dup2(w2, stdout)
        os.execvp(cmd2[0], cmd2)
    os.close(w)
    os.close(r)
    os.waitpid(pid, 0)

    r3,  w3 = os.pipe() 
    pid = os.fork()
    if pid == 0:
        os.close(w2)
        os.close(r3)
        os.dup2(r2, stdin)
        os.dup2(w3, stdout)
        os.execvp(cmd3[0], cmd3)
    os.close(r2)
    os.close(w2)
    os.waitpid(pid, 0)

    pid = os.fork()
    if pid == 0:
        os.close(w3)
        os.dup2(r3, stdin)
        os.execvp(cmd4[0], cmd4)
    os.close(r3)
    os.close(w3)
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

exex_command(["echo", "Hello"], ["cat", "-e"], ["head", "-n 10"], ["less", "-"])
