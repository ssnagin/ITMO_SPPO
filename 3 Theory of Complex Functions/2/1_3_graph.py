import numpy as np
import matplotlib.pyplot as plt

def f_original(x):
    """Исходная функция: f(x) = sin(x) * |cos(x)|"""
    return np.sin(x) * np.abs(np.cos(x))

def fourier_coeffs_analytic(N):
    """
    Аналитически вычисляет коэффициенты Фурье для f(x) = sin(x) * |cos(x)|
    на интервале [-π, π] (период 2π).
    
    Возвращает:
        a0: float (всегда 0)
        an: массив a_0, a_1, ..., a_N (все нули)
        bn: массив b_0, b_1, ..., b_N
        cn: массив c_{-N}, ..., c_0, ..., c_N (длина 2N+1)
    """
    # Инициализация
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    a0 = 0.0
    bn[0] = 0.0  # b0 не используется, но для согласованности

    # Вычисление b_n для n = 1 ... N
    for n in range(1, N + 1):
        if n == 2:
            bn[n] = 0.0
        else:
            bn[n] = (4.0 / (np.pi * (4 - n**2))) * np.sin(n * np.pi / 2.0)
        an[n] = 0.0  # функция нечётная

    # Комплексные коэффициенты c_n для n = -N ... N
    cn = np.zeros(2 * N + 1, dtype=complex)
    cn[N] = a0 / 2.0  # c_0 = 0

    for n in range(1, N + 1):
        c_pos = -1j * bn[n] / 2.0      # c_n = -i b_n / 2
        c_neg = 1j * bn[n] / 2.0       # c_{-n} = conjugate(c_n) = +i b_n / 2 (т.к. b_n веществен)
        cn[N + n] = c_pos
        cn[N - n] = c_neg

    return a0, an, bn, cn

def partial_sum_trig(x, a0, an, bn, N):
    """Тригонометрическая частичная сумма до N-й гармоники"""
    result = np.full_like(x, a0 / 2.0, dtype=float)
    for n in range(1, N + 1):
        result += an[n] * np.cos(n * x) + bn[n] * np.sin(n * x)
    return result

def partial_sum_complex(x, cn, N):
    """Комплексная частичная сумма до N-й гармоники"""
    result = np.zeros_like(x, dtype=complex)
    for k in range(-N, N + 1):
        idx = k + N
        result += cn[idx] * np.exp(1j * k * x)
    return result.real  # мнимая часть должна быть ~0

# --------------------------
# Основной блок визуализации
# --------------------------
if __name__ == "__main__":
    # Диапазон построения: два периода для лучшей видимости
    x_plot = np.linspace(-2 * np.pi, 2 * np.pi, 2000)
    f_true = f_original(x_plot)

    N_values = [1, 2, 5, 10, 20]
    plt.figure(figsize=(14, 10))

    for i, N in enumerate(N_values, 1):
        a0, an, bn, cn = fourier_coeffs_analytic(N)
        F_N = partial_sum_trig(x_plot, a0, an, bn, N)
        G_N = partial_sum_complex(x_plot, cn, N)

        plt.subplot(3, 2, i)
        plt.plot(x_plot, f_true, 'k-', linewidth=2, label=r'$f(x) = \sin x \, |\cos x|$')
        plt.plot(x_plot, F_N, 'b--', linewidth=1.5, label=f'Триг. сумма, N={N}')
        plt.plot(x_plot, G_N, 'r:', linewidth=1.5, label=f'Компл. сумма, N={N}')
        plt.title(f'Частичная сумма при N = {N}', fontsize=12)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.ylim(-1.1, 1.1)
        plt.grid(True, linestyle=':', alpha=0.7)
        if i == 1:
            plt.legend(loc='upper right')

    plt.tight_layout()
    plt.suptitle(r'Аппроксимация функции $f(x) = \sin x \, |\cos x|$ частичными суммами ряда Фурье', y=1.02, fontsize=14)
    plt.show()