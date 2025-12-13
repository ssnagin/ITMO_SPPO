import numpy as np

# Определяем квадратную волну на периоде [pi, 3pi)
def f_square(t):
    # Приводим t к основному периоду [pi, 3pi)
    T = 2 * np.pi
    t_mod = (t - np.pi) % T + np.pi  # сдвигаем в [pi, 3pi)
    return np.where(t_mod < 2*np.pi, 1.0, 2.0)

# Функция для численного вычисления коэффициентов при заданном N
def fourier_coeffs_numeric(N):
    T = 2 * np.pi
    t0 = np.pi
    t1 = t0 + T
    # Мелкая сетка для точного интегрирования
    t = np.linspace(t0, t1, 2000, endpoint=False)
    dt = t[1] - t[0]
    f_vals = f_square(t)
    
    # a0
    a0 = (2 / T) * np.sum(f_vals) * dt
    
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    
    for n in range(1, N + 1):
        cos_nt = np.cos(n * t)
        sin_nt = np.sin(n * t)
        an[n] = (2 / T) * np.sum(f_vals * cos_nt) * dt
        bn[n] = (2 / T) * np.sum(f_vals * sin_nt) * dt
    
    # Комплексные коэффициенты c_n для n = -N ... N
    cn = np.zeros(2 * N + 1, dtype=complex)
    cn[N] = a0 / 2  # c0
    for n in range(1, N + 1):
        cn[N + n] = (an[n] - 1j * bn[n]) / 2  # c_n
        cn[N - n] = (an[n] + 1j * bn[n]) / 2  # c_{-n}
    
    return a0, an, bn, cn

# --- РАСЧЁТ ДЛЯ N = 2 ---
N = 2
a0_num, an_num, bn_num, cn_num = fourier_coeffs_numeric(N)

print("=== Сравнение: ручной расчёт vs численный (N=2) ===")
print(f"a0: ручной = 3.0000, численный = {a0_num:.4f}")
print(f"a1: ручной = 0.0000, численный = {an_num[1]:.4f}")
print(f"a2: ручной = 0.0000, численный = {an_num[2]:.4f}")
print(f"b1: ручной = {2/np.pi:.4f}, численный = {bn_num[1]:.4f}")
print(f"b2: ручной = 0.0000, численный = {bn_num[2]:.4f}")
print("\nКомплексные коэффициенты (численно):")
for n in range(-N, N+1):
    idx = n + N
    print(f"c_{n:>2} = {cn_num[idx]: .4f}") 
