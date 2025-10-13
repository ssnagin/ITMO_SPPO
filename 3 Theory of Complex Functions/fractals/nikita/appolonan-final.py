import numpy as np
from PIL import Image
import math
import cmath

# ==============================================================================
# КОНСТАНТЫ И НАСТРОЙКИ СЕТКИ
# ==============================================================================
SIZE = 6001  # Размер сетки N x N
MAX_DEPTH = 8  # Глубина рекурсии (оставим 2 для быстрой проверки)
PIXEL_GRID = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # Сетка RGB (Черный фон)
CENTER = SIZE // 2  # CENTER = 500
SCALE_FACTOR = CENTER * 0.95  # Коэффициент масштаба для отступов
K0_GLOBAL = -1.0  # Кривизна внешней окружности
Z0_GLOBAL = complex(0.0, 0.0)  # Центр внешней окружности


# ==============================================================================
# ГЕОМЕТРИЧЕСКИЕ ФУНКЦИИ (Сохранены без изменений)
# ==============================================================================

def find_new_curvatures(k1, k2, k3):
    """Вычисляет кривизны k_plus и k_minus (Теорема Декарта)."""
    radicand = k1 * k2 + k2 * k3 + k3 * k1
    root = math.sqrt(max(0, radicand))
    sum_k = k1 + k2 + k3
    k_plus = sum_k + 2 * root
    k_minus = sum_k - 2 * root
    return k_plus, k_minus


def find_new_center(k1, k2, k3, z1, z2, z3, k_new):
    """Вычисляет центры z_plus и z_minus (Формула Содди)."""
    sum_terms = k1 * z1 * k2 * z2 + k2 * z2 * k3 * z3 + k3 * z3 * k1 * z1
    root_val = cmath.sqrt(sum_terms)
    sum_kz = k1 * z1 + k2 * z2 + k3 * z3
    z_plus = (sum_kz + 2 * root_val) / k_new
    z_minus = (sum_kz - 2 * root_val) / k_new
    return z_plus, z_minus


# ==============================================================================
# ФУНКЦИЯ ВИЗУАЛИЗАЦИИ
# ==============================================================================

def draw_disc(k, z, color):
    """Отрисовывает закрашенный круг (диск) на пиксельной сетке."""
    r_new = abs(1.0 / k)
    x_new, y_new = z.real, z.imag

    pixel_x_center = CENTER + x_new * SCALE_FACTOR
    pixel_y_center = CENTER - y_new * SCALE_FACTOR
    pixel_r = r_new * SCALE_FACTOR

    # Определение границ для ускорения отрисовки
    x_min = max(0, int(pixel_x_center - pixel_r))
    x_max = min(SIZE, int(pixel_x_center + pixel_r + 1))
    y_min = max(0, int(pixel_y_center - pixel_r))
    y_max = min(SIZE, int(pixel_y_center + pixel_r + 1))

    # Проверка расстояния для закрашивания
    r_sq = pixel_r * pixel_r
    for py in range(y_min, y_max):
        for px in range(x_min, x_max):
            dx = px - pixel_x_center
            dy = py - pixel_y_center
            if dx * dx + dy * dy <= r_sq:
                PIXEL_GRID[py, px] = color


# ==============================================================================
# НОВЫЕ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ СЛУЧАЯ C0
# ==============================================================================

def get_k_inner_boundary(k_plus, k_minus, k_current_trio):
    """Возвращает k_new, которая заполняет промежуток. Для k0=-1 это всегда k_plus."""
    if K0_GLOBAL in k_current_trio:
        return k_plus
    else:
        # Для внутренних троек выбираем k с наибольшей кривизной
        return max(k_plus, k_minus)


def get_z_inner_boundary(k_new, k_trio, z_trio, z_plus, z_minus):
    """
    ИСПРАВЛЕННЫЙ МЕТОД: Выбирает центр, который наиболее точно
    соответствует условию касания C0 (расстояние = R0 - r_new).
    """

    r_new = 1.0 / k_new
    R0 = 1.0

    # Требуемое расстояние от z_new до z0 для касания C0
    REQUIRED_DIST = R0 - r_new

    # Фактические расстояния
    dist_plus = abs(z_plus - Z0_GLOBAL)
    dist_minus = abs(z_minus - Z0_GLOBAL)

    # Разница между фактическим и требуемым расстоянием
    error_plus = abs(dist_plus - REQUIRED_DIST)
    error_minus = abs(dist_minus - REQUIRED_DIST)

    # Выбираем центр с наименьшей ошибкой
    if error_plus < error_minus:
        return z_plus
    else:
        return z_minus

    # Примечание: Мы опускаем проверку "None" из предыдущей версии,
    # поскольку k_new уже выбрано как решение, заполняющее промежуток.


# ==============================================================================
# УНИВЕРСАЛЬНАЯ РЕКУРСИВНАЯ ФУНКЦИЯ
# ==============================================================================

def apollonian_gasket_recursive(k1, k2, k3, z1, z2, z3, depth, color):
    """
    Универсальная рекурсивная функция.
    """
    if depth >= MAX_DEPTH:
        return

    k_trio = (k1, k2, k3)
    z_trio = (z1, z2, z3)

    # 1. Находим две новые кривизны
    k_plus, k_minus = find_new_curvatures(k1, k2, k3)

    # --- ЛОГИКА ВЫБОРА k_new ---
    if K0_GLOBAL in k_trio:
        k_new = get_k_inner_boundary(k_plus, k_minus, k_trio)
    else:
        k_new = max(k_plus, k_minus)

    if k_new > 10000.0 or k_new < 0.01:
        return

    # 2. Находим центры
    # ИСПРАВЛЕНИЕ ОШИБКИ: Явно передаем все 6 аргументов (k1-k3, z1-z3) + k_new
    z_plus, z_minus = find_new_center(k1, k2, k3, z1, z2, z3, k_new)

    # 3. --- ЛОГИКА ВЫБОРА z_new ---
    if K0_GLOBAL in k_trio:
        z_new = get_z_inner_boundary(k_new, k_trio, z_trio, z_plus, z_minus)
    else:
        # Старая логика (эвристика ближайшего к центроиду) - для внутренних троек
        avg_z = sum(z_trio) / 3
        z_new = z_plus if abs(z_plus - avg_z) < abs(z_minus - avg_z) else z_minus

    if z_new is None:
        return

    # 4. ВИЗУАЛИЗАЦИЯ
    draw_disc(k_new, z_new, color)

    # 5. РЕКУРСИВНЫЕ ВЫЗОВЫ
    next_depth = depth + 1
    next_color = [(color[0] + 40) % 256, (color[1] + 20) % 256, (color[2] + 60) % 256]

    # Важно: Передаем полные списки аргументов
    apollonian_gasket_recursive(k1, k2, k_new, z1, z2, z_new, next_depth, next_color)
    apollonian_gasket_recursive(k1, k_new, k3, z1, z_new, z3, next_depth, next_color)
    apollonian_gasket_recursive(k_new, k2, k3, z_new, z2, z3, next_depth, next_color)


def main():
    """Основная функция, устанавливающая начальные условия и запускающая процесс."""

    k0, z0 = K0_GLOBAL, Z0_GLOBAL
    # Кривизна C1, C2, C3
    k_in = 1 + 2 * math.sqrt(3) / 3.0
    # Расстояние центра от z0: R0 - r_in
    r_c = 1.0 - abs(1 / k_in)

    # Центры C1, C2, C3, расположенные симметрично
    z1 = complex(r_c, 0.0)
    z2 = complex(r_c * math.cos(2 * math.pi / 3), r_c * math.sin(2 * math.pi / 3))
    z3 = complex(r_c * math.cos(4 * math.pi / 3), r_c * math.sin(4 * math.pi / 3))

    # 1. Отрисовка исходных окружностей (Фон и "скелет")
    draw_disc(k0, z0, [255, 255, 255])  # C0 (Белый фон)
    draw_disc(k_in, z1, [50, 50, 50])  # C1 (Серый)
    draw_disc(k_in, z2, [50, 50, 50])  # C2 (Серый)
    draw_disc(k_in, z3, [50, 50, 50])  # C3 (Серый)

    # 2. Запуск рекурсии

    # Центральный промежуток (C1, C2, C3)
    apollonian_gasket_recursive(k_in, k_in, k_in, z1, z2, z3, 0, [255, 0, 0])

    # Внешние промежутки (C0, Ci, Cj)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z1, z2, 0, [0, 255, 0])
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z2, z3, 0, [0, 0, 255])
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z3, z1, 0, [255, 255, 0])

    # 3. Сохранение результата
    img = Image.fromarray(PIXEL_GRID, 'RGB')
    img.save("apollonian_gasket_final_precision.png")
    print(
        f"Построение завершено. Изображение сохранено как 'apollonian_gasket_final_precision.png' с глубиной {MAX_DEPTH}.")


if __name__ == "__main__":
    main()