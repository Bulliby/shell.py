import os

r, w = os.pipe()

class Pipe():
    def __init__(self, cmd, first = False, last = False):
        self.cmd = cmd
        self.first = first
        self.r, self.w = os.pipe()
        self.r2, self.w2 = os.pipe()
        if first:
            self.first_command()
        elif last:
            self.last_command()
        else:
            self.middle_commands()


    def first_command(self):
        pid = os.fork()
        if pid == 0:
            os.close(self.r)
            os.dup2(self.w, 1)
            os.execvp(self.cmd, [self.cmd])

    def middle_commands(self):
        self.r2, self.w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.dup2(self.r, 0)
            os.close(self.r2)
            os.dup2(self.w2, 1)
            os.execvp(self.cmd, [self.cmd])


    def last_command(self):
        pid = os.fork()
        if pid == 0:
            os.close(self.w2)
            os.dup2(self.r2, 0)
            os.execvp(self.cmd, [self.cmd])

