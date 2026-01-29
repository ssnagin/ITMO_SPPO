import numpy as np

def fourier_coefficients(N):
    """
    Аналитически вычисляет коэффициенты Фурье для f(t) = cos(t) - sin^2(t)
    на интервале длины T = 2π.
    """
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    cn = np.zeros(N + 1, dtype=complex)

    an[0] = -1.0
    bn[0] = 0.0
    cn[0] = an[0] / 2

    for n in range(1, N + 1):
        if n == 1:
            an[n] = 1.0
        elif n == 2:
            an[n] = 0.5
        else:
            an[n] = 0.0

        bn[n] = 0.0 

        cn[n] = (an[n] - 1j * bn[n]) / 2

    return an, bn, cn

N = 2
a_coeffs, b_coeffs, c_coeffs = fourier_coefficients(N)

print("Коэффициенты Фурье для N=2:")
print("a_n:", a_coeffs)
print("b_n:", b_coeffs)
print("c_n:", c_coeffs)

print("\nКонкретно для n=2:")
print("a_2 =", a_coeffs[2])
print("b_2 =", b_coeffs[2])
print("c_2 =", c_coeffs[2])