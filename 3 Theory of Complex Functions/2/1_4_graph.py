import numpy as np
import matplotlib.pyplot as plt

# Исходная функция
def f_func(x):
    return np.abs(np.sin(x) + np.cos(2 * x))

def fourier_coeffs_numeric(N):
    """
    Численно вычисляет коэффициенты Фурье для f(x) = |sin x + cos 2x| 
    на интервале [-π, π] с периодом 2π.
    """
    T = 2 * np.pi
    x0, x1 = -np.pi, np.pi
    num_points = 10000
    x = np.linspace(x0, x1, num_points, endpoint=False)
    dx = x[1] - x[0]
    f_vals = f_func(x)

    a0 = (2 / T) * np.sum(f_vals) * dx

    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)

    for n in range(1, N + 1):
        an[n] = (2 / T) * np.sum(f_vals * np.cos(n * x)) * dx
        bn[n] = (2 / T) * np.sum(f_vals * np.sin(n * x)) * dx

    return a0, an, bn

def partial_sum_trig(x, a0, an, bn, N):
    """Частичная сумма Фурье до гармоники N"""
    result = np.full_like(x, a0 / 2, dtype=float)
    for n in range(1, N + 1):
        result += an[n] * np.cos(n * x) + bn[n] * np.sin(n * x)
    return result

if __name__ == "__main__":
    x_plot = np.linspace(-2 * np.pi, 2 * np.pi, 2000)
    f_true = f_func(x_plot)

    N_values = [1, 2, 3, 4, 10]
    plt.figure(figsize=(14, 12))

    for i, N in enumerate(N_values, 1):
        a0, an, bn = fourier_coeffs_numeric(N)
        f_approx = partial_sum_trig(x_plot, a0, an, bn, N)

        plt.subplot(3, 2, i)
        plt.plot(x_plot, f_true, 'k-', linewidth=2.0, label=r'$f(x) = |\sin x + \cos 2x|$')
        plt.plot(x_plot, f_approx, 'r--', linewidth=1.5, label=rf'$S_{{{N}}}(x)$')
        plt.title(f'Частичная сумма Фурье: N = {N}', fontsize=12)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.ylim(-0.1, 1.5)
        plt.grid(True, linestyle=':', alpha=0.7)
        if i == 1:
            plt.legend(loc='upper right')

    plt.tight_layout()
    plt.suptitle('Разложение $f(x) = |\\sin x + \\cos 2x|$ в ряд Фурье', y=1.02, fontsize=14)
    plt.show()