import numpy as np
import matplotlib.pyplot as plt

a, b = 1, 2
t0, t1, t2 = np.pi, 2*np.pi, 3*np.pi

# Отдельные сегменты — НИКАКИХ соединений
plt.figure(figsize=(10, 2.5))

# Слева от t0 — 0 (необязательно, если не нужно)
# plt.hlines(b, 0, t0, colors='b', linewidth=2)

# Сегмент 1: [t0, t1) = 1
# plt.hlines(a, t0, t1, colors='b', linewidth=2)

# Сегмент 2: [t1, t2] = 2
# plt.hlines(b, t1, t2, colors='b', linewidth=2)

# Справа от t2 — 0 (если нужно)
# plt.hlines(a, t2, 4*np.pi, colors='b', linewidth=2)

def draw_lines(plt: plt, i : int = 3):
    for i in range(i):
        # Сегмент 1: [t0, t1) = 1
        plt.hlines(a, t0 + (i*np.pi), t1 + (i*np.pi), colors='b', linewidth=2)

        # Сегмент 2: [t1, t2] = 2
        # plt.hlines(b, t1*(i + 1), t2*(i + 1), colors='b', linewidth=2)

draw_lines(plt, 3)

# Настройки
plt.grid(True, linestyle='--', alpha=0.6)
plt.title('f(t), a = 1, b = 2, t0 = pi, t1 = 2pi, t2 = 3pi')
plt.xlabel('t')
plt.ylabel('f(t)')
plt.yticks([0, 1, 2])
plt.xticks([0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi],
           ['0', 'π', '2π', '3π', '4π'])
plt.ylim(-0.2, 2.5)
plt.xlim(-0.5, 4*np.pi)
plt.tight_layout()
plt.show()