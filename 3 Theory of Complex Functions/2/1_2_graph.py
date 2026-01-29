import numpy as np
import matplotlib.pyplot as plt


def f_cos_minus_sin2(t):
    """
    Функция f(t) = cos(t) - sin^2(t)
    Период: 2π
    """
    return np.cos(t) - np.sin(t)**2


def fourier_coeffs_numeric(N):
    """
    Вычисляет коэффициенты Фурье для f(t) = cos(t) - sin^2(t) на [0, 2π) с периодом T = 2π.
    Возвращает a0, an[0..N], bn[0..N], cn[-N..N] (массив длины 2N+1).
    """
    T = 2 * np.pi
    t0 = 0.0
    t1 = T

    num_points = 5000
    t = np.linspace(t0, t1, num_points, endpoint=False)
    dt = t[1] - t[0]
    f_vals = f_cos_minus_sin2(t)
    
    # a0 = (2 / T) * ∫ f(t) dt → но стандартная формула: a0 = (1/π) ∫_{-π}^{π} f(t) dt
    # Однако при интегрировании на [0, 2π]: a0 = (1/π) ∫_0^{2π} f(t) dt
    # Но в коде ниже используется общий подход: a0 = (2/T) * ∫ f(t) dt → что эквивалентно (1/π) ∫_0^{2π}
    a0 = (2 / T) * np.sum(f_vals) * dt
    
    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)
    
    for n in range(1, N + 1):
        an[n] = (2 / T) * np.sum(f_vals * np.cos(n * t)) * dt
        bn[n] = (2 / T) * np.sum(f_vals * np.sin(n * t)) * dt
    
    # Комплексные коэффициенты c_n для n = -N, ..., N
    cn = np.zeros(2 * N + 1, dtype=complex)
    cn[N] = a0 / 2  # c_0
    for n in range(1, N + 1):
        cn[N + n] = (an[n] - 1j * bn[n]) / 2   # c_n
        cn[N - n] = (an[n] + 1j * bn[n]) / 2   # c_{-n}
    
    return a0, an, bn, cn


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
        idx = k + N 
        result += cn[idx] * np.exp(1j * k * t)
    return result.real


if __name__ == "__main__":
    # Диапазон для построения графика (несколько периодов для наглядности)
    t_plot = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    f_true = f_cos_minus_sin2(t_plot)

    # Поскольку функция — тригонометрический полином степени 2,
    # достаточно N=2 для точного восстановления.
    N_values = [0, 1, 2, 3, 5]
    
    plt.figure(figsize=(14, 10))

    for i, N in enumerate(N_values, 1):
        a0, an, bn, cn = fourier_coeffs_numeric(N)
        F_N = partial_sum_trig(t_plot, a0, an, bn, N)
        G_N = partial_sum_complex(t_plot, cn, N)
        
        plt.subplot(3, 2, i)
        plt.plot(t_plot, f_true, 'k-', linewidth=2, label=r'$f(t) = \cos t - \sin^2 t$')
        plt.plot(t_plot, F_N, 'b--', linewidth=1.5, label=f'$F_N(t)$, N={N}')
        plt.plot(t_plot, G_N, 'r:', linewidth=1.5, label=f'$G_N(t)$, N={N}')
        plt.title(f'N = {N}', fontsize=12)
        plt.xlabel('t')
        plt.ylabel('f(t)')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.ylim(-2, 2)
        if i == 1:
            plt.legend()

    plt.tight_layout()
    plt.suptitle(r'Частичные суммы ряда Фурье для $f(t) = \cos t - \sin^2 t$', y=1.02, fontsize=14)
    plt.show()

    # Выведем найденные коэффициенты для N=5
    a0, an, bn, cn = fourier_coeffs_numeric(5)
    print("Найденные коэффициенты:")
    print(f"a0 = {a0:.6f}")
    for n in range(1, 6):
        print(f"a_{n} = {an[n]:.6f},   b_{n} = {bn[n]:.6f}")