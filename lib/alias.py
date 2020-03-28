from numba import jit

@jit(nopython=True)
def normalize(alias):
    alias=alias.replace(' ', '')
    alias=alias.replace('-', '')
    alias=alias.strip()
    return alias