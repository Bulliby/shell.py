import os

class IPCChain():

    def __init__(self):
        self.r, self.w = os.pipe()
        self.r2 = False 
        self.w2 = False

    def start_chain(self, node):
        print("start")
        pid = os.fork()
        if pid == 0:
            os.close(self.r)
            # Close stdout and duplicate w. (w is now stdout)
            os.dup2(self.w, 1)
            os.execvp(node.cmd, node.suffix)
        os.waitpid(pid, 0)

    def pipe_inter(self, cmd):
        print("inter")
        self.r2, self.w2 = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(self.w)
            os.close(self.r2)
            # Close stdin and duplicate r. (r is now stdin)
            os.dup2(self.r, 0)
            os.dup2(self.w2, 1)
            os.execvp(cmd.cmd, cmd.suffix)
        os.close(self.w)
        os.close(self.r)
        self.r = self.r2
        self.w = self.w2
        os.waitpid(pid, 0)

    def pipe_end(self, cmd):
        print("end")
        if self.r2 != False:
            pid = os.fork()
            if pid == 0:
                os.close(self.w2)
                os.dup2(self.r2, 0)
                os.execvp(cmd.cmd, cmd.suffix)
            os.close(self.r2)
            os.close(self.w2)
        else:
            pid = os.fork()
            if pid == 0:
                os.close(self.w)
                os.dup2(self.r, 0)
                os.execvp(cmd.cmd, cmd.suffix)
            os.close(self.r)
            os.close(self.w)
        os.waitpid(pid, 0)

