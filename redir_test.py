import os

def exec_command(cmd1, cmd2):
    r, w = os.pipe()

    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.dup2(w, 1)
        os.execvp(cmd1, [cmd1])
    
    os.wait()
    os.close(w)
    os.dup2(r, 0)
    fd = os.open("test.txt", os.O_RDWR)
    buf = os.read(0, 1000)
    while buf:
        os.write(fd, buf)
        buf = os.read(0, 1000)

    """"
    r = os.fdopen(r)
    buf = r.read(1000)
    print("buf", buf)
    fd = os.open("test.txt", os.O_WRONLY)
    os.write(fd, buf)
    """

exec_command('ls', 'wc')
