import os

def exec_command(cmd1, cmd2, file):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.dup2(w, 1)
        os.execvp(cmd1, [cmd1])
    
    r2, w2 = os.pipe()
    pid2 = os.fork()
    if pid2 == 0:
        os.close(w)
        os.dup2(r, 0)
        os.close(r2)
        os.dup2(w2, 1)
        os.execvp(cmd2, [cmd2])

    os.close(w2)
    os.close(r)
    os.close(w)
    os.dup2(r2, 0)
    fd = os.open(file, os.O_RDWR)
    buf = os.read(0, 1)
    while buf:
        os.write(fd, buf)
        buf = os.read(0, 1)

exec_command('ls', 'wc', 'toto')
