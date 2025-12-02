import numpy as np
from PIL import Image
import math
import cmath  # Используем cmath для комплексного квадратного корня, чтобы быть чище

# === КОНСТАНТЫ СЕТКИ И ВИЗУАЛИЗАЦИИ ===
SIZE = 10001  # Размер сетки N x N (нечетное число для центра)
MAX_DEPTH = 10  # Максимальная глубина рекурсии (около 6-7 уже дают хороший фрактал)
PIXEL_GRID = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # Сетка RGB
CENTER = SIZE // 2


# === ГЕОМЕТРИЧЕСКИЕ ФУНКЦИИ (Теорема Декарта и Содди) ===

def find_new_curvatures(k1, k2, k3):
    """Вычисляет кривизны двух окружностей, касающихся трех заданных."""
    # Избегаем math.sqrt для отрицательных значений, которые могут
    # возникнуть из-за ошибок округления, когда значение очень близко к 0.
    radicand = k1 * k2 + k2 * k3 + k3 * k1
    root = math.sqrt(max(0, radicand))

    sum_k = k1 + k2 + k3

    # Теорема Декарта: k_новая = sum_k ± 2*sqrt(k1*k2 + k2*k3 + k3*k1)
    k_plus = sum_k + 2 * root
    k_minus = sum_k - 2 * root

    return k_plus, k_minus


def find_new_center(k1, k2, k3, z1, z2, z3, k_new):
    """
    Вычисляет центр z_new (комплексное число) новой окружности по Формуле Содди.
    z_i - центр окружности i как комплексное число (x + iy)
    """

    # Расширенная Теорема Декарта (Формула Содди)
    # k_новая*z_новая = k1*z1 + k2*z2 + k3*z3 ± 2*sqrt(k1*z1*k2*z2 + k2*z2*k3*z3 + k3*z3*k1*z1)

    # Вычисляем члены под комплексным квадратным корнем
    sum_terms = k1 * z1 * k2 * z2 + k2 * z2 * k3 * z3 + k3 * z3 * k1 * z1

    # Комплексный квадратный корень
    # Используем cmath для комплексного квадратного корня
    root_val = cmath.sqrt(sum_terms)

    sum_kz = k1 * z1 + k2 * z2 + k3 * z3

    # Два решения для центра:
    z_plus = (sum_kz + 2 * root_val) / k_new
    z_minus = (sum_kz - 2 * root_val) / k_new

    return z_plus, z_minus


# === ФУНКЦИЯ РЕКУРСИИ ===

def apollonian_gasket_recursive(k1, k2, k3, z1, z2, z3, depth, color):
    """
    Рекурсивная функция для построения ковра Аполлония,
    отрисовывающая только центры окружностей.
    """
    if depth >= MAX_DEPTH:
        return

    # 1. Находим две новые кривизны
    k_plus, k_minus = find_new_curvatures(k1, k2, k3)

    # Выбираем k_new, которая соответствует меньшей окружности (большая кривизна)
    # или которая находится внутри (если k0 < 0).
    k_new = max(k_plus, k_minus)

    # Проверка на вырожденный случай (линия или слишком большая окружность)
    if k_new < 0.01:
        return

    # 2. Находим два центра для k_new
    z_plus, z_minus = find_new_center(k1, k2, k3, z1, z2, z3, k_new)

    # 3. Выбираем правильный центр
    # Эвристика: выбираем центр, который находится ближе к "среднему" центру.
    avg_z = (z1 + z2 + z3) / 3
    if abs(z_plus - avg_z) < abs(z_minus - avg_z):
        z_new = z_plus
    else:
        z_new = z_minus

    # === ИСПРАВЛЕННАЯ ВИЗУАЛИЗАЦИЯ (ТОЛЬКО ЦЕНТР) ===
    x_new, y_new = z_new.real, z_new.imag

    # Масштабирование и преобразование координат (от -1..1 до 0..SIZE)
    # Предполагаем, что фрактал умещается в квадрате от -1 до 1.
    scale = CENTER * 0.95  # Коэффициент масштаба
    pixel_x = int(CENTER + x_new * scale)
    pixel_y = int(CENTER - y_new * scale)  # Инвертируем Y для соответствия матрице

    # Закрашиваем только один пиксель, если он находится в пределах сетки
    if 0 <= pixel_x < SIZE and 0 <= pixel_y < SIZE:
        PIXEL_GRID[pixel_y, pixel_x] = color

        # === 4. РЕКУРСИВНЫЕ ВЫЗОВЫ ===

    # Переход к следующей глубине и новому цвету
    next_depth = depth + 1

    # Изменяем цвет для визуализации итераций
    # (Используем HSV-подобное смещение для лучшего контраста)
    next_color = [(color[0] + 40) % 256, (color[1] + 20) % 256, (color[2] + 60) % 256]

    # Новые тройки для рекурсии:

    # 1. Тройка (k1, k2, k_new)
    apollonian_gasket_recursive(k1, k2, k_new, z1, z2, z_new, next_depth, next_color)

    # 2. Тройка (k1, k3, k_new)
    apollonian_gasket_recursive(k1, k_new, k3, z1, z_new, z3, next_depth, next_color)

    # 3. Тройка (k2, k3, k_new)
    apollonian_gasket_recursive(k_new, k2, k3, z_new, z2, z3, next_depth, next_color)


def main():
    # === НАЧАЛЬНЫЕ УСЛОВИЯ ===

    # C0: Ограничивающая окружность (радиус 1, кривизна -1, центр 0)
    k0 = -1.0
    z0 = complex(0.0, 0.0)

    # C1, C2, C3: Три равные внутренние окружности, касающиеся C0
    # Для симметрии и упрощения используем классические кривизны k=3,
    # а центры вычислим для случая, когда C1, C2, C3 касаются друг друга и C0.
    # Если k0=-1, k1=k2=k3=3, то центры должны быть на расстоянии 2/3 от начала координат.
    k_in = 3.0

    # Расстояние центра от z0: r_c = 1 - r_in = 1 - 1/3 = 2/3
    r_c = 2.0 / 3.0

    # Центры C1, C2, C3, расположенные симметрично
    z1 = complex(r_c, 0.0)
    z2 = complex(r_c * math.cos(2 * math.pi / 3), r_c * math.sin(2 * math.pi / 3))
    z3 = complex(r_c * math.cos(4 * math.pi / 3), r_c * math.sin(4 * math.pi / 3))

    # Рекурсия вызывается для трех внешних промежутков:

    # 1. Промежуток (C0, C1, C2)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z1, z2, 0, [255, 0, 0])

    # 2. Промежуток (C0, C2, C3)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z2, z3, 0, [0, 255, 0])

    # 3. Промежуток (C0, C3, C1)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z3, z1, 0, [0, 0, 255])

    # === СОХРАНЕНИЕ РЕЗУЛЬТАТА ===
    img = Image.fromarray(PIXEL_GRID, 'RGB')
    img.save("apollonian_gasket_centers.png")
    print(
        f"Построение завершено. Изображение сохранено как 'apollonian_gasket_centers.png' с глубиной {MAX_DEPTH}. Отрисованы только центры окружностей.")


if __name__ == "__main__":
    main()