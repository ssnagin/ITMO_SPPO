import numpy as np
from PIL import Image
import math
import cmath

# === КОНСТАНТЫ СЕТКИ И ВИЗУАЛИЗАЦИИ ===
SIZE = 8001  # Размер сетки N x N (нечетное число для центра)
MAX_DEPTH = 2 # Максимальная глубина рекурсии (около 6-7 уже дают хороший фрактал)
PIXEL_GRID = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # Сетка RGB (Начнем с черного фона)
CENTER = (SIZE // 2) + 1
SCALE_FACTOR = CENTER * 1  # Коэффициент масштаба для преобразования координат


# === ГЕОМЕТРИЧЕСКИЕ ФУНКЦИИ (Теорема Декарта и Содди) ===

def find_new_curvatures(k1, k2, k3):
    """Вычисляет кривизны двух окружностей, касающихся трех заданных."""
    radicand = k1 * k2 + k2 * k3 + k3 * k1
    root = math.sqrt(max(0, radicand))

    sum_k = k1 + k2 + k3

    k_plus = sum_k + 2 * root
    k_minus = sum_k - 2 * root

    return k_plus, k_minus


def find_new_center(k1, k2, k3, z1, z2, z3, k_new):
    """Вычисляет центр z_new (комплексное число) новой окружности по Формуле Содди."""
    sum_terms = k1 * z1 * k2 * z2 + k2 * z2 * k3 * z3 + k3 * z3 * k1 * z1
    root_val = cmath.sqrt(sum_terms)

    sum_kz = k1 * z1 + k2 * z2 + k3 * z3

    z_plus = (sum_kz + 2 * root_val) / k_new
    z_minus = (sum_kz - 2 * root_val) / k_new

    return z_plus, z_minus


# === ФУНКЦИЯ РЕКУРСИИ ===

def apollonian_gasket_recursive(k1, k2, k3, z1, z2, z3, depth, color):
    """
    Рекурсивная функция для построения ковра Аполлония,
    отрисовывающая закрашенные окружности.
    """
    if depth >= MAX_DEPTH:
        return

    # 1. Находим новую кривизну
    k_plus, k_minus = find_new_curvatures(k1, k2, k3)
    k_new = max(k_plus, k_minus)

    # Проверка на вырожденный случай или слишком маленькие окружности
    if k_new < 0.01 or k_new > 10000:  # k_new > 10000 для предотвращения ошибок float
        return

    # 2. Находим центр
    z_plus, z_minus = find_new_center(k1, k2, k3, z1, z2, z3, k_new)

    # Выбираем центр (эвристика)
    avg_z = (z1 + z2 + z3) / 3
    if abs(z_plus - avg_z) < abs(z_minus - avg_z):
        z_new = z_plus
    else:
        z_new = z_minus

    # === НОВЫЙ БЛОК ВИЗУАЛИЗАЦИИ: ОТРИСОВКА ОКРУЖНОСТИ ===
    x_new, y_new = z_new.real, z_new.imag
    r_new = 1.0 / k_new

    # Пиксельные координаты центра и радиуса
    pixel_x_center = CENTER + x_new * SCALE_FACTOR
    pixel_y_center = CENTER - y_new * SCALE_FACTOR  # Инвертируем Y
    pixel_r = r_new * SCALE_FACTOR

    # Определяем границы квадрата, в который вписана окружность
    x_min = int(pixel_x_center - pixel_r)
    x_max = int(pixel_x_center + pixel_r)
    y_min = int(pixel_y_center - pixel_r)
    y_max = int(pixel_y_center + pixel_r)

    # Ограничиваем границы сеткой
    x_min = max(0, x_min)
    x_max = min(SIZE, x_max)
    y_min = max(0, y_min)
    y_max = min(SIZE, y_max)

    # Закрашиваем только те пиксели, которые находятся внутри окружности
    # for py in range(y_min, y_max):
    #     for px in range(x_min, x_max):
    #         # Проверка расстояния от пикселя (px, py) до центра (pixel_x_center, pixel_y_center)
    #         dx = px - pixel_x_center
    #         dy = py - pixel_y_center
    #         # Если расстояние меньше радиуса (длина вектора dx, dy)
    #         if dx * dx + dy * dy <= pixel_r * pixel_r:
    #             # Мы закрашиваем только то, что еще не закрашено (или закрашиваем поверх)
    #             # Здесь мы просто закрашиваем, чтобы показать диск
    #             PIXEL_GRID[py, px] = color

    #             # === 4. РЕКУРСИВНЫЕ ВЫЗОВЫ ===

    next_depth = depth + 1

    # Изменяем цвет для визуализации итераций
    next_color = [(color[0] + 40) % 256, (color[1] + 20) % 256, (color[2] + 60) % 256]

    # Новые тройки для рекурсии:

    # 1. Тройка (k1, k2, k_new)
    apollonian_gasket_recursive(k1, k2, k_new, z1, z2, z_new, next_depth, next_color)

    # 2. Тройка (k1, k3, k_new)
    apollonian_gasket_recursive(k1, k_new, k3, z1, z_new, z3, next_depth, next_color)

    # 3. Тройка (k2, k3, k_new)
    apollonian_gasket_recursive(k_new, k2, k3, z_new, z2, z3, next_depth, next_color)

'''
def main():
    # === НАЧАЛЬНЫЕ УСЛОВИЯ ===

    # C0: Ограничивающая окружность (радиус 1, кривизна -1, центр 0)
    k0 = -1.0
    z0 = complex(0.0, 0.0)

    # C1, C2, C3: Три равные внутренние окружности, касающиеся C0
    k_in = 2.0 / (2 * math.sqrt(3) - 3)

    # Центры для трех равных окружностей (радиус 1/3)
    r_c = 1 - k_in # Расстояние центра от (0,0)

    # Центры C1, C2, C3, расположенные симметрично
    z1 = complex(r_c, 0.0)
    z2 = complex(r_c * math.cos(2 * math.pi / 3), r_c * math.sin(2 * math.pi / 3))
    z3 = complex(r_c * math.cos(4 * math.pi / 3), r_c * math.sin(4 * math.pi / 3))

    # Отрисовываем исходные три окружности (Шаг 0)
    # Это важно, так как рекурсия начинается с поиска окружностей внутри промежутков,
    # а сами C1, C2, C3 остаются неокрашенными.
    initial_circles = [
        (k0, z0, [255, 255, 255]),  # Внешняя (белый фон)
        (k_in, z1, [50, 50, 50]),  # Внутренняя 1
        (k_in, z2, [50, 50, 50]),  # Внутренняя 2
        (k_in, z3, [50, 50, 50]),  # Внутренняя 3
    ]

    # Изолированная функция для рисования диска
    def draw_disc(k, z, color):
        x_new, y_new = z.real, z.imag
        r_new = abs(1.0 / k)

        pixel_x_center = CENTER + x_new * SCALE_FACTOR
        pixel_y_center = CENTER - y_new * SCALE_FACTOR
        pixel_r = r_new * SCALE_FACTOR

        x_min = max(0, int(pixel_x_center - pixel_r))
        x_max = min(SIZE, int(pixel_x_center + pixel_r))
        y_min = max(0, int(pixel_y_center - pixel_r))
        y_max = min(SIZE, int(pixel_y_center + pixel_r))

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                dx = px - pixel_x_center
                dy = py - pixel_y_center
                if dx * dx + dy * dy <= pixel_r * pixel_r:
                    PIXEL_GRID[py, px] = color

    # Рисуем ограничивающую окружность C0 (белый фон)
    draw_disc(k0, z0, [255, 255, 255])

    # Рисуем три внутренние окружности C1, C2, C3 (серый цвет)
    draw_disc(k_in, z1, [50, 50, 50])
    draw_disc(k_in, z2, [50, 50, 50])
    draw_disc(k_in, z3, [50, 50, 50])

    # Запускаем рекурсию для заполнения промежутков

    # 1. Промежуток (C0, C1, C2)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z1, z2, 0, [255, 0, 0])

    # 2. Промежуток (C0, C2, C3)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z2, z3, 0, [0, 255, 0])

    # 3. Промежуток (C0, C3, C1)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z3, z1, 0, [0, 0, 255])

    # === СОХРАНЕНИЕ РЕЗУЛЬТАТА ===
    img = Image.fromarray(PIXEL_GRID, 'RGB')
    img.save("apollonian_gasket_discs.png")
    print(
        f"Построение завершено. Изображение сохранено как 'apollonian_gasket_discs.png' с глубиной {MAX_DEPTH}. Отрисованы закрашенные диски.")
'''


def main():
    # === НАЧАЛЬНЫЕ УСЛОВИЯ ===

    # C0: Ограничивающая окружность (радиус 1, кривизна -1, центр 0)
    k0 = -1.0
    z0 = complex(0.0, 0.0)

    # C1, C2, C3: Три равные внутренние окружности, касающиеся C0
    k_in = 2

    # Центры для трех равных окружностей (радиус 1/3)
    r_c = 1.0 / 2.0 # Расстояние центра от (0,0)

    # Центры C1, C2, C3, расположенные симметрично
    z1 = complex(r_c, 0.0)
    z2 = complex(r_c * -1, 0.0)

    # Отрисовываем исходные три окружности (Шаг 0)
    # Это важно, так как рекурсия начинается с поиска окружностей внутри промежутков,
    # а сами C1, C2, C3 остаются неокрашенными.
    initial_circles = [
        (k0, z0, [255, 255, 255]),  # Внешняя (белый фон)
        (k_in, z1, [50, 50, 50]),  # Внутренняя 1
        (k_in, z2, [50, 50, 50]),  # Внутренняя 2
    ]

    # Изолированная функция для рисования диска
    def draw_disc(k, z, color):
        x_new, y_new = z.real, z.imag
        r_new = abs(1.0 / k)

        pixel_x_center = CENTER + x_new * SCALE_FACTOR
        pixel_y_center = CENTER + y_new * SCALE_FACTOR
        pixel_r = r_new * SCALE_FACTOR

        x_min = max(0, int(pixel_x_center - pixel_r))
        x_max = min(SIZE, int(pixel_x_center + pixel_r))
        y_min = max(0, int(pixel_y_center - pixel_r))
        y_max = min(SIZE, int(pixel_y_center + pixel_r))

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                dx = px - pixel_x_center
                dy = py - pixel_y_center
                if dx * dx + dy * dy <= pixel_r * pixel_r:
                    PIXEL_GRID[py, px] = color

    # Рисуем ограничивающую окружность C0 (белый фон)
    draw_disc(k0, z0, [255, 255, 255])

    # Рисуем три внутренние окружности C1, C2, C3 (серый цвет)
    draw_disc(k_in, z1, [50, 50, 50])
    # draw_disc(k_in, z2, [50, 50, 50])
    draw_disc(k_in, z2, [50, 50, 50])
    # draw_disc(k_in, z3, [50, 50, 50])

    # Запускаем рекурсию для заполнения промежутков

    # 1. Промежуток (C0, C1, C2)
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z1, z2, 0, [255, 0, 0])

    # === СОХРАНЕНИЕ РЕЗУЛЬТАТА ===
    img = Image.fromarray(PIXEL_GRID, 'RGB')
    img.save("apollonian_gasket_discs.png")
    print(
        f"Построение завершено. Изображение сохранено как 'apollonian_gasket_discs.png' с глубиной {MAX_DEPTH}. Отрисованы закрашенные диски.")


if __name__ == "__main__":
    main()