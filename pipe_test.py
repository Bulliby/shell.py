import os

def exex_command(cmd1, cmd2, cmd3, cmd4):
    r, w = os.pipe()
    print("firstPipe r: {0}, w: {1}".format(r,w))
    pid = os.fork()
    if pid == 0:
        print(cmd1)
        os.close(r)
        os.dup2(w, 1)
        os.execvp(cmd1, [cmd1])

    r2, w2 = os.pipe()
    pid2 = os.fork()
    if pid2 == 0:
        print(cmd2)
        os.close(w)
        os.dup2(r, 0)
        os.close(r2)
        os.dup2(w2, 1)
        os.execvp(cmd2, [cmd2])

    r3, w3 = os.pipe()
    pid3 = os.fork()
    if pid3 == 0:
        print(cmd3)
        os.close(w2)
        os.dup2(r2, 0)
        os.close(r3)
        os.dup2(w3, 1)
        os.execvp(cmd3, [cmd3])

    pid3 = os.fork()
    if pid3 == 0:
        print(cmd3)
        os.close(w3)
        os.dup2(r3, 0)
        os.execvp(cmd3, [cmd3])
    else:
        os.wait()

exex_command("ls", "wc", "wc", "wc")
