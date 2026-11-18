import ctypes
from numba import njit
from numba.extending import get_cython_function_address
import levy_noise

print("levy_noise module:", levy_noise.__file__)
addr = get_cython_function_address("levy_noise", "levy_noise")
functype = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)
c_levy = functype(addr)
print("C function address OK:", addr)

for dll in (None, "msvcrt.dll", "ucrtbase.dll", "vcruntime140.dll"):
    try:
        (ctypes.CDLL(None) if dll is None else ctypes.CDLL(dll)).srand(42)
        print("srand OK via:", dll if dll else "CDLL(None)")
    except Exception as e:
        print("srand FAIL via:", dll, "->", str(e)[:60])

@njit
def trial(alpha, dt):
    return c_levy(alpha, dt)
print("njit->C sample:", round(trial(1.5, 0.001), 6))

def seq():
    ctypes.CDLL("msvcrt.dll").srand(42)
    return [round(c_levy(1.5, 0.001), 8) for _ in range(5)]
s1, s2 = seq(), seq()
print("reproducible:", s1 == s2, s1)
