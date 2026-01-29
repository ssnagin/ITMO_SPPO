import numpy as np

def fourier_coefficients(N):
    """
    Аналитически вычисляет коэффициенты Фурье для f(x) = sin(x) * |cos(x)|
    на интервале [-π, π] (период 2π).
    
    Возвращает:
        an: массив a_0, a_1, ..., a_N  (все нули)
        bn: массив b_0, b_1, ..., b_N  (b_0 = 0, остальные по формуле)
        cn: массив c_0, c_1, ..., c_N  (комплексные коэффициенты)
    """
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    cn = np.zeros(N + 1, dtype=complex)

    # a_0 и все a_n = 0 (функция нечётная)
    an[0] = 0.0

    # b_0 не используется в разложении, но положим 0
    bn[0] = 0.0
    cn[0] = 0.0  # c_0 = 0

    for n in range(1, N + 1):
        # Вычисляем b_n по аналитической формуле
        if n == 2:
            bn[n] = 0.0
        else:
            bn[n] = (4.0 / (np.pi * (4 - n**2))) * np.sin(n * np.pi / 2.0)
        
        # Все a_n = 0
        an[n] = 0.0

        # Комплексный коэффициент: c_n = (a_n - i b_n) / 2 = -i b_n / 2
        cn[n] = -1j * bn[n] / 2.0

    return an, bn, cn


# Пример использования
N = 10
a_coeffs, b_coeffs, c_coeffs = fourier_coefficients(N)

print("Коэффициенты Фурье для f(x) = sin(x) * |cos(x)| (N = {}):".format(N))
print("a_n:", a_coeffs)
print("b_n:", b_coeffs)
print("c_n:", c_coeffs)

print("\nНенулевые b_n (не чётные n):")
for n in range(1, N + 1):
    if abs(b_coeffs[n]) > 1e-12:
        print(f"b_{n} = {b_coeffs[n]:.6f}")