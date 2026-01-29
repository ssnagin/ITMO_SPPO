import numpy as np
import matplotlib.pyplot as plt

def f_func(x):
    return np.abs(np.sin(x) + np.cos(2 * x))

def fourier_coeffs_numeric(N):
    T = 2 * np.pi
    x0, x1 = -np.pi, np.pi
    num_points = 20000
    x = np.linspace(x0, x1, num_points, endpoint=False)
    dx = x[1] - x[0]
    f_vals = f_func(x)

    # Полная энергия
    energy_full = (1 / np.pi) * np.sum(f_vals**2) * dx

    # a0
    a0 = (2 / T) * np.sum(f_vals) * dx

    an = np.zeros(N + 1)
    bn = np.zeros(N + 1)

    for n in range(1, N + 1):
        an[n] = (2 / T) * np.sum(f_vals * np.cos(n * x)) * dx
        bn[n] = (2 / T) * np.sum(f_vals * np.sin(n * x)) * dx

    return a0, an, bn, energy_full

def parseval_energy(a0, an, bn, N):
    """Вычисляет сумму квадратов коэффициентов до N"""
    energy = (a0**2) / 2.0
    for n in range(1, N + 1):
        energy += an[n]**2 + bn[n]**2
    return energy

if __name__ == "__main__":
    N_values = [1, 2, 3, 4, 10]

    # Вычислим полную энергию один раз (достаточно с большим N, например 50)
    _, _, _, energy_true = fourier_coeffs_numeric(50)

    print(f"Полная энергия (по Парсевалю, N→∞):  E = {energy_true:.12f}")
    print("-" * 60)
    print(f"{'N':<3} {'E_N (накоплено)':<20} {'Относ. ошибка (%)':<20}")
    print("-" * 60)

    for N in N_values:
        a0, an, bn, _ = fourier_coeffs_numeric(N)
        E_N = parseval_energy(a0, an, bn, N)
        rel_error = 100 * (energy_true - E_N) / energy_true
        print(f"{N:<3} {E_N:<20.12f} {rel_error:<20.6f}")


    N_max = 30
    Ns = np.arange(1, N_max + 1)
    E_Ns = []

    for N in Ns:
        a0, an, bn, _ = fourier_coeffs_numeric(N)
        E_Ns.append(parseval_energy(a0, an, bn, N))

    plt.figure(figsize=(8, 5))
    plt.plot(Ns, E_Ns, 'bo-', label=r'$E_N = \frac{a_0^2}{2} + \sum_{n=1}^N (a_n^2 + b_n^2)$')
    plt.axhline(energy_true, color='r', linestyle='--', label=r'Полная энергия $E$')
    plt.xlabel('N (макс. гармоника)')
    plt.ylabel('Энергия')
    plt.title('Сходимость равенства Парсеваля')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.show()