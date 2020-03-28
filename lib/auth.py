from lib import reply, numbers
from numba import jit

@jit(nopython=True)
def valid(num, msgreply):
    num=numbers.normalize(num)
    print(num)
    if reply.getNumberGroup(num) is not None:
        status = reply.getAuth(reply.getNumberGroup(num), msgreply)
    else:
        status = False
    return status