# **************************************************************************** #
#                                                                              #
#                                                                              #
#    HandleProcesses.py                                                        #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2023/09/29 13:09:00 by bulliby            \     \_\ \     /      #
#    Updated: 2023/09/29 13:09:02 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import sys
import os

class HandleProcesses():

    def waitProcess(self, pid):
        """
        Used in Boolean operator shell "&& ||"
        """
        status = os.waitpid(pid, 0)[1]
        if os.WIFEXITED(status):
            return os.WEXITSTATUS(status)
        return 0

    def exec(self, node):
        """
        https://docs.python.org/3/library/os.html#process-parameters
        flush them using sys.stdout.flush() or os.fsync() before calling an exec* function
        """
        sys.stdout.flush()
        try:
            os.execvp(node.cmd, node.suffix)
        except FileNotFoundError:
            print("Command {0} not found".format(node.cmd))
            exit(42)
