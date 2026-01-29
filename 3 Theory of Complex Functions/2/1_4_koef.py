import numpy as np
from scipy.integrate import quad


def f(x):
    return np.abs(np.sin(x) + np.cos(2 * x))

def a0():
    integral, _ = quad(f, -np.pi, np.pi)
    return (1 / np.pi) * integral

def an(n):
    integrand = lambda x: f(x) * np.cos(n * x)
    integral, _ = quad(integrand, -np.pi, np.pi)
    return (1 / np.pi) * integral

def bn(n):
    integrand = lambda x: f(x) * np.sin(n * x)
    integral, _ = quad(integrand, -np.pi, np.pi)
    return (1 / np.pi) * integral

Ns = [1, 2, 3, 4, 10]

print(f"a0/2 = {a0()/2:.12f}\n")

for N in Ns:
    a = an(N)
    b = bn(N)
    print(f"N = {N:2d} → a_{N:2d} = {a: .12f},   b_{N:2d} = {b: .12f}")