from numba import jit

@jit(nopython=True)
def normalize(num):
    num=num.replace('+','')
    num=num.replace('-','')
    num=num.replace(' ','')
    num=num.strip()
    return num