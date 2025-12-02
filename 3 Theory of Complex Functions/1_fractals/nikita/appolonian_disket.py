import numpy as np
from PIL import Image
import math
import cmath

# ==============================================================================
# КОНСТАНТЫ И НАСТРОЙКИ СЕТКИ
# ==============================================================================
SIZE = 1001  # Размер сетки N x N
MAX_DEPTH = 4 # Глубина рекурсии (7-8 оптимально для 1001x1001)
PIXEL_GRID = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # Сетка RGB (Черный фон)
CENTER = SIZE // 2 + 1
SCALE_FACTOR = CENTER * 0.95  # Коэффициент масштаба для отступов


# ==============================================================================
# ГЕОМЕТРИЧЕСКИЕ ФУНКЦИИ (Теорема Декарта и Содди)
# ==============================================================================

def find_new_curvatures(k1, k2, k3):
    """Вычисляет кривизны двух окружностей, касающихся трех заданных."""
    radicand = k1 * k2 + k2 * k3 + k3 * k1
    root = math.sqrt(max(0, radicand))

    sum_k = k1 + k2 + k3

    # Теорема Декарта
    k_plus = sum_k + 2 * root
    k_minus = sum_k - 2 * root

    return k_plus, k_minus


def find_new_center(k1, k2, k3, z1, z2, z3, k_new):
    """Вычисляет центр z_new (комплексное число) новой окружности по Формуле Содди."""
    # Комплексный член под корнем
    sum_terms = k1 * z1 * k2 * z2 + k2 * z2 * k3 * z3 + k3 * z3 * k1 * z1
    root_val = cmath.sqrt(sum_terms)

    sum_kz = k1 * z1 + k2 * z2 + k3 * z3

    # Два решения для центра
    z_plus = (sum_kz + 2 * root_val) / k_new
    z_minus = (sum_kz - 2 * root_val) / k_new

    return z_plus, z_minus


# ==============================================================================
# ФУНКЦИЯ ВИЗУАЛИЗАЦИИ
# ==============================================================================

def draw_disc(k, z, color):
    """Отрисовывает закрашенный круг (диск) на пиксельной сетке."""
    # Учет знака кривизны (для радиуса)
    r_new = abs(1.0 / k)
    x_new, y_new = z.real, z.imag

    # Преобразование в пиксельные координаты
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
# РЕКУРСИВНАЯ ФУНКЦИЯ ПОСТРОЕНИЯ
# ==============================================================================

def apollonian_gasket_recursive(k1, k2, k3, z1, z2, z3, depth, color):
    """Рекурсивный вызов для нахождения и отрисовки новой окружности."""
    if depth >= MAX_DEPTH:
        return

    # 1. Находим новую кривизну. Берем большую (меньший радиус)
    k_plus, k_minus = find_new_curvatures(k1, k2, k3)
    k_new = max(k_plus, k_minus)

    # Условие остановки для очень маленьких окружностей
    if k_new > 10000.0:
        return

    # 2. Находим центр
    z_plus, z_minus = find_new_center(k1, k2, k3, z1, z2, z3, k_new)

    # # 3. Выбираем правильный центр (эвристика: ближайший к центроиду)
    # avg_z = (z1 + z2 + z3) / 3
    # if abs(z_plus - avg_z) < abs(z_minus - avg_z):
    #     z_new = z_plus
    # else:
    #     z_new = z_minus

    # 3. Выбираем правильный центр (критерий: наличие отрицательной кривизны )
    if any(k < 0 for k in [k1, k2, k3]):
        z_new = z_plus  # Для внешних промежутков (с C0) нужен z_plus
    else:
        z_new = z_minus  # Для внутренних промежутков (три положительные кривизны) нужен z_minus

    # 4. ВИЗУАЛИЗАЦИЯ: Отрисовываем найденную окружность
    draw_disc(k_new, z_new, color)
    print(depth, k_new, z_new, color)

    # 5. РЕКУРСИВНЫЕ ВЫЗОВЫ

    next_depth = depth + 1
    # Сдвиг цвета для следующей итерации
    next_color = [(color[0] + 40) % 256, (color[1] + 20) % 256, (color[2] + 60) % 256]

    # Создаются ТРИ новые тройки для рекурсии (заполнение трех новых промежутков)

    # Тройка (k1, k2, k_new)
    apollonian_gasket_recursive(k1, k2, k_new, z1, z2, z_new, next_depth, next_color)

    # Тройка (k1, k3, k_new)
    apollonian_gasket_recursive(k1, k_new, k3, z1, z_new, z3, next_depth, next_color)

    # Тройка (k2, k3, k_new)
    apollonian_gasket_recursive(k_new, k2, k3, z_new, z2, z3, next_depth, next_color)


def main():
    """Основная функция, устанавливающая начальные условия и запускающая процесс."""

    # Начальные условия: C0 (внешняя) и C1, C2, C3 (внутренние, попарно касающиеся)

    # C0: Ограничивающая окружность (R=1, k=-1, z=0)
    k0 = -1.0
    z0 = complex(0.0, 0.0)

    # C1, C2, C3: Внутренние окружности (R = 2*sqrt(3) - 3, k = 1 + 2*sqrt(3)/3)
    k_in = 1 + 2 * math.sqrt(3) / 3.0  # Кривизна
    r_c = 1.0 - abs(1 / k_in)  # Расстояние центра от z0

    # Центры C1, C2, C3, расположенные симметрично на углах треугольника
    z1 = complex(r_c, 0.0)
    z2 = complex(r_c * math.cos(2 * math.pi / 3), r_c * math.sin(2 * math.pi / 3))
    z3 = complex(r_c * math.cos(4 * math.pi / 3), r_c * math.sin(4 * math.pi / 3))

    # 1. Отрисовка исходных окружностей (Фон и "скелет")
    draw_disc(k0, z0, [255, 255, 255])  # C0 (Белый фон)
    draw_disc(k_in, z1, [50, 50, 50])  # C1 (Серый)
    draw_disc(k_in, z2, [50, 50, 50])  # C2 (Серый)
    draw_disc(k_in, z3, [50, 50, 50])  # C3 (Серый)

    # 2. Запуск рекурсии для заполнения трех внешних промежутков

    apollonian_gasket_recursive(k_in, k_in, k_in, z1, z2, z3, 0, [255, 0, 0])

    apollonian_gasket_recursive(k0, k_in, k_in, z0, z1, z2, 0, [255, 0, 0]) # GPT посмотри здесь
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z2, z3, 0, [255, 0, 0])
    apollonian_gasket_recursive(k0, k_in, k_in, z0, z3, z1, 0, [255, 0, 0])


    # 3. Сохранение результата
    img = Image.fromarray(PIXEL_GRID, 'RGB')
    img.save("apollonian_gasket_final.png")
    print(f"Построение завершено. Изображение сохранено как 'apollonian_gasket_final.png' с глубиной {MAX_DEPTH}.")


if __name__ == "__main__":
    main()