"""
benchmark.py — Compare Python pur vs C/ctypes pour le calcul de la moyenne
Usage : python benchmark.py
"""

import time
import random
import c_bridge as C

N = 1_000_000
data = [random.gauss(50, 10) for _ in range(N)]
print(f"Tableau de {N:,} valeurs générées.")
print("-" * 45)

# ── Python pur ────────────────────────────────────────────────────
start = time.perf_counter()
mean_py = sum(data) / len(data)
elapsed_py = time.perf_counter() - start
print(f"Python pur  : moyenne = {mean_py:.4f}  [{elapsed_py*1000:.2f} ms]")

# ── C via ctypes ──────────────────────────────────────────────────
start = time.perf_counter()
mean_c = C.moyenne(data)
elapsed_c = time.perf_counter() - start
print(f"C / ctypes  : moyenne = {mean_c:.4f}  [{elapsed_c*1000:.2f} ms]")

print("-" * 45)
if elapsed_c > 0:
    print(f"Gain de vitesse : x{elapsed_py/elapsed_c:.1f}")
