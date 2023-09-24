# **************************************************************************** #
#                                                                              #
#                                                                              #
#    Boolean.py                                                                #
#                                                         ________             #
#    By: bulliby <wellsguillaume+at+gmail.com>           /   ____/_  _  __     #
#                                                       /    \  _\ \/ \/ /     #
#    Created: 2019/05/25 19:21:40 by bulliby            \     \_\ \     /      #
#    Updated: 2019/05/30 12:09:40 by bulliby             \________/\/\_/       #
#                                                                              #
# **************************************************************************** #

import os

"""
Used in Boolean operator shell "&& ||"
"""

class WaitProcess():

    def waitProcess(self, pid):
        status = os.waitpid(pid, 0)[1]
        if os.WIFEXITED(status):
            return os.WEXITSTATUS(status)
        return 0

