import os

r, w = os.pipe()

class Pipe():
    def __init__(self, cmd, first):
        self.cmd = cmd
        self.first = first
        self.exec_command()

    def exec_command(self):
        global r
        global w
        pid = os.fork()
        if pid == 0:
            #First type of child process
            if self.first == False:
                print(self.cmd)
                os.close(r)
                os.dup2(w, 1)
                os.execvp(self.cmd, [self.cmd])
            #Second type of child process
            else:
                print(self.cmd)
                os.close(w)
                os.dup2(r, 0)
                os.execvp(self.cmd, [self.cmd])

        else: #father process
            if self.first == False:
                os.waitpid(pid, 0)
