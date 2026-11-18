import ctypes
from numba.extending import get_cython_function_address
import levy_noise

addr = get_cython_function_address("levy_noise", "levy_noise")
functype = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)
c_levy = functype(addr)

def draw():
    return [round(c_levy(1.5, 0.001), 8) for _ in range(5)]

# Establish a reference sequence after seeding a given DLL
for dll_name in ("ucrtbase.dll", "msvcrt.dll"):
    dll = ctypes.CDLL(dll_name)
    try:
        dll.srand.argtypes = [ctypes.c_uint]
        dll.srand.restype = None
    except Exception as e:
        print(dll_name, "srand setup failed", e)
        continue
    dll.srand(42)
    a = draw()
    dll.srand(42)
    b = draw()
    print(f"{dll_name}: self-repeat={a==b}  seq={a}")

# Cross-check: does ucrt srand control what msvcrt srand produced?
u = ctypes.CDLL("ucrtbase.dll"); u.srand.argtypes=[ctypes.c_uint]
m = ctypes.CDLL("msvcrt.dll"); m.srand.argtypes=[ctypes.c_uint]
u.srand(42); ua = draw()
m.srand(42); ma = draw()
print("ucrt-seed result:", ua)
print("msvcrt-seed result:", ma)
print("same underlying RNG?", ua == ma)
