import numpy as np
import matplotlib.pyplot as plt

def fourier_coefficients(N, a=1, b=2, t0=np.pi, t1=2*np.pi, t3=3*np.pi):
    an = np.zeros(N+1)
    bn = np.zeros(N+1)
    cn = np.zeros(N+1, dtype=complex)
    
    for n in range(N+1):
        if n == 0:
            an[0] = (1/(t3 - t0)) * (1*(t1 - t0) + 2*(t3 - t1))
            bn[0] = 0
            cn[0] = an[0] / 2
        else:
            integral_an = (1/(t3 - t0)) * (np.sin(n*t1) - np.sin(n*t0) + 2*(np.sin(n*t3) - np.sin(n*t1))) / n
            integral_bn = (1/(t3 - t0)) * (-np.cos(n*t1) + np.cos(n*t0) + 2*(-np.cos(n*t3) + np.cos(n*t1))) / n
            an[n] = integral_an
            bn[n] = integral_bn
            cn[n] = (an[n] - 1j*bn[n]) / 2
    
    return an, bn, cn

N = 2
a_coeffs, b_coeffs, c_coeffs = fourier_coefficients(N)

print("Коэффициенты Фурье для N=2:")
print("a_n:", a_coeffs[2])
print("b_n:", b_coeffs[2])
print("c_n:", c_coeffs[2])
