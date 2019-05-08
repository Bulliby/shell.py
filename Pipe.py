import os

class Pipe():

    def __init__(self):
        self.r, self.w = os.pipe()

    def exec_pipe(self, cmd):
        if type(cmd) is str:
            r2, w2 = os.pipe()
            pid = os.fork()
            if pid == 0:
                os.close(self.w)
                os.dup2(self.r, 0)
                os.close(r2)
                os.dup2(w2, 1)
                os.execvp(cmd, [cmd])

            self.r = r2
            self.w = w2
