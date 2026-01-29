
import numpy as np
# Проверка Парсеваля
def parseval_check(N_max=1000):
    # Левая часть (точно)
    left = 1/4
    
    # Правая часть (частичная сумма)
    right = 0.0
    for n in range(1, N_max + 1):
        if n == 2:
            bn = 0.0
        else:
            bn = (4.0 / (np.pi * (4 - n**2))) * np.sin(n * np.pi / 2.0)
        right += bn**2
    
    print(f"Левая часть (точная): {left:.10f}")
    print(f"Правая часть (N={N_max}): {right:.10f}")
    print(f"Разница: {abs(left - right):.2e}")

parseval_check(1000)