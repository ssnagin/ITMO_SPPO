import mpmath as mp

def f(x):
    return abs(mp.sin(x) + mp.cos(2*x))

# Period is 2*pi, interval [-pi, pi]
L = mp.pi

def a_n(n):
    integrand = lambda x: f(x) * mp.cos(n*x)
    return (1/mp.pi) * mp.quad(integrand, [-mp.pi, mp.pi])

def b_n(n):
    integrand = lambda x: f(x) * mp.sin(n*x)
    return (1/mp.pi) * mp.quad(integrand, [-mp.pi, mp.pi])

a0 = a_n(0)
a1 = a_n(1)
a2 = a_n(2)
a3 = a_n(3)
b1 = b_n(1)
b2 = b_n(2)
b3 = b_n(3)

print(a0, a1, a2, a3, b1, b2, b3)