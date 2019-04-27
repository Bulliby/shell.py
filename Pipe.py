import os

class Pipe():
    def __init__(self, cmd, pipe):
        self.cmd = cmd
        self.pipe = pipe
        if self.pipe == None:
            self.r, self.w = os.pipe()
        else:
            self.r = pipe.r
            self.w = pipe.w

    def exec_pipe(self):
        r2, w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.dup2(self.r, 0)
            os.close(r2)
            os.dup2(w2, 1)
            os.execvp(self.cmd, [self.cmd])

        self.r = r2
        self.w = w2
        return self
