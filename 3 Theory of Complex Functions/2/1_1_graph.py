import numpy as np
import matplotlib.pyplot as plt

# === 1. Определение квадратной волны ===
def f_square(t):
    """
    Квадратная волна с периодом 2π:
    f(t) = 1 на [π, 2π), f(t) = 2 на [2π, 3π)
    Функция периодически продолжается на всю числовую ось.
    """
    T = 2 * np.pi
    # Приводим t к базовому периоду [π, 3π)
    t_shifted = t - np.pi  # сдвигаем, чтобы период начинался с 0
    t_mod = np.mod(t_shifted, T)  # берём по модулю периода
    t_in_base = t_mod + np.pi     # возвращаем в [π, 3π)
    return np.where(t_in_base < 2 * np.pi, 1.0, 2.0)

# === 2. Численное вычисление коэффициентов Фурье ===
def fourier_coeffs_numeric(N):
    """
    Вычисляет коэффициенты Фурье для квадратной волны на [π, 3π) с периодом T=2π.
    Возвращает a0, an[0..N], bn[0..N], cn[-N..N] (в виде массива длины 2N+1).
    """
    T = 2 * np.pi
    t0 = np.pi
    t1 = t0 + T
    # Используем плотную сетку для точного численного интегрирования
    num_points = 5000
    t = np.linspace(t0, t1, num_points, endpoint=False)
    dt = t[1] - t[0]
    f_vals = f_square(t)
    
    # a0
    a0 = (2 / T) * np.sum(f_vals) * dt
    
    # Массивы для an и bn (индекс 0 не используется для n>=1, но оставим для удобства)
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    
    for n in range(1, N + 1):
        an[n] = (2 / T) * np.sum(f_vals * np.cos(n * t)) * dt
        bn[n] = (2 / T) * np.sum(f_vals * np.sin(n * t)) * dt
    
    # Комплексные коэффициенты c_n для n = -N, ..., 0, ..., N
    cn = np.zeros(2 * N + 1, dtype=complex)
    cn[N] = a0 / 2  # c_0
    for n in range(1, N + 1):
        cn[N + n] = (an[n] - 1j * bn[n]) / 2   # c_{+n}
        cn[N - n] = (an[n] + 1j * bn[n]) / 2   # c_{-n}
    
    return a0, an, bn, cn

# === 3. Частичные суммы ряда ===
def partial_sum_trig(t, a0, an, bn, N):
    """Тригонометрическая частичная сумма F_N(t)"""
    result = np.full_like(t, a0 / 2, dtype=float)
    for n in range(1, N + 1):
        result += an[n] * np.cos(n * t) + bn[n] * np.sin(n * t)
    return result

def partial_sum_complex(t, cn, N):
    """Комплексная частичная сумма G_N(t)"""
    result = np.zeros_like(t, dtype=complex)
    for k in range(-N, N + 1):
        idx = k + N  # индекс в массиве cn[0...2N]
        result += cn[idx] * np.exp(1j * k * t)
    return result.real  # мнимая часть ≈ 0 из-за симметрии

# === 4. Построение графиков ===
if __name__ == "__main__":
    # Диапазон для построения (один период)
    t_plot = np.linspace(np.pi, 3 * np.pi, 1000)
    f_true = f_square(t_plot)

    N_values = [1, 2, 5, 10, 20]
    plt.figure(figsize=(14, 10))

    for i, N in enumerate(N_values, 1):
        a0, an, bn, cn = fourier_coeffs_numeric(N)
        F_N = partial_sum_trig(t_plot, a0, an, bn, N)
        G_N = partial_sum_complex(t_plot, cn, N)
        
        plt.subplot(3, 2, i)
        plt.plot(t_plot, f_true, 'k-', linewidth=2, label='f(t)')
        plt.plot(t_plot, F_N, 'b--', linewidth=1.5, label=f'F_N(t), N={N}')
        plt.plot(t_plot, G_N, 'r:', linewidth=1.5, label=f'G_N(t), N={N}')
        plt.title(f'N = {N}', fontsize=12)
        plt.xlabel('t')
        plt.ylabel('f(t)')
        plt.ylim(0.5, 2.5)
        plt.grid(True, linestyle=':', alpha=0.7)
        if i == 1:
            plt.legend()

    plt.tight_layout()
    plt.suptitle('Аппроксимация квадратной волны частичными суммами ряда Фурье', y=1.02)
    plt.show()
