import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from collections import deque
import argparse # Импортируем argparse

def solve_soddy_curvature(k1, k2, k3):
    """
    Вычисляет кривизну вписанной окружности Содди по теореме Декарта.
    """
    sum_k = k1 + k2 + k3
    # Используем np.complex для безопасного вычисления корня
    sqrt_term = 2 * np.sqrt(np.complex128(k1 * k2 + k2 * k3 + k3 * k1))
    return sum_k + sqrt_term.real

def solve_soddy_center(k1, k2, k3, k4, z1, z2, z3):
    """
    Вычисляет центр вписанной окружности Содди по комплексной теореме Декарта.
    """
    sum_kz = k1 * z1 + k2 * z2 + k3 * z3
    sqrt_term = 2 * np.sqrt(k1 * z1 * k2 * z2 + k2 * z2 * k3 * z3 + k3 * z3 * k1 * z1)

    z4_candidate1 = (sum_kz + sqrt_term) / k4
    z4_candidate2 = (sum_kz - sqrt_term) / k4

    if (np.abs(z4_candidate1 - z1) > 1e-9 and
        np.abs(z4_candidate1 - z2) > 1e-9 and
        np.abs(z4_candidate1 - z3) > 1e-9):
        return z4_candidate1
    else:
        return z4_candidate2

def generate_apollonian_gasket(max_iterations=10000, min_radius=0.005):
    """
    Генерирует набор окружностей для Ковра Аполлония.
    """
    # Начальная конфигурация
    k1, z1 = -1.0, 0 + 0j
    k2, z2 = 2.0, 0.5 + 0j
    k3, z3 = 2.0, -0.5 + 0j
    
    # Ключ для канонической сортировки
    sort_key = lambda c: (c[0], c[1].real, c[1].imag)
    
    initial_triplet = tuple(sorted(((k1, z1), (k2, z2), (k3, z3)), key=sort_key))
    
    tasks = deque([initial_triplet])
    processed_tasks = {initial_triplet}
    
    iterations = 0
    while tasks and iterations < max_iterations:
        iterations += 1
        
        current_triplet = tasks.popleft()
        k1_c, z1_c = current_triplet[0]
        k2_c, z2_c = current_triplet[1]
        k3_c, z3_c = current_triplet[2]

        k4 = solve_soddy_curvature(k1_c, k2_c, k3_c)
        
        if k4 <= 0 or 1 / k4 < min_radius:
            continue
            
        z4 = solve_soddy_center(k1_c, k2_c, k3_c, k4, z1_c, z2_c, z3_c)
        c4_data = (k4, z4)

        new_triplets_to_process = [
            (current_triplet[0], current_triplet[1], c4_data),
            (current_triplet[0], current_triplet[2], c4_data),
            (current_triplet[1], current_triplet[2], c4_data)
        ]
        
        for triplet in new_triplets_to_process:
            sorted_triplet = tuple(sorted(triplet, key=sort_key))
            if sorted_triplet not in processed_tasks:
                tasks.append(sorted_triplet)
                processed_tasks.add(sorted_triplet)

    # Собираем все уникальные окружности из обработанных троек
    unique_circles = {item for triplet in processed_tasks for item in triplet}
    
    circles_to_plot = []
    for k, z in unique_circles:
        radius = np.abs(1 / k)
        circles_to_plot.append((z.real, z.imag, radius))
        
    return circles_to_plot

def plot_gasket(circles, output=None):
    """Отрисовывает сгенерированные окружности."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    for x, y, radius in circles:
        is_outer = radius > 0.99
        edgecolor = 'black'
        facecolor = 'white' if not is_outer else 'lightgray'
        linewidth = 1.5 if is_outer else 1
        zorder = 1 if is_outer else 2
        
        circle_patch = Circle((x, y), radius, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth, zorder=zorder)
        ax.add_patch(circle_patch)
        
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_title("Ковёр Аполлония (Apollonian Gasket)", fontsize=16)
    
    if output:
        plt.savefig(output, dpi=200, bbox_inches='tight')
        print(f"Изображение сохранено в '{output}'")
    else:
        plt.show()

def main():
    """
    Главная функция для парсинга аргументов и запуска генерации.
    """
    parser = argparse.ArgumentParser(description="Визуализация Ковра Аполлония (Apollonian Gasket)")
    
    parser.add_argument('--max_iter', type=int, default=15000, 
                        help='Максимальное число итераций (обрабатываемых троек окружностей)')
    parser.add_argument('--min_radius', type=float, default=0.003, 
                        help='Минимальный радиус окружности для генерации')
    parser.add_argument('--output', type=str, default=None, 
                        help='Имя файла для сохранения изображения (например: apollonian.png)')
    
    args = parser.parse_args()

    print("Генерация Ковра Аполлония...")
    print(f"Параметры: max_iter={args.max_iter}, min_radius={args.min_radius}")
    
    apollonian_circles = generate_apollonian_gasket(
        max_iterations=args.max_iter,
        min_radius=args.min_radius
    )
    
    print(f"Сгенерировано {len(apollonian_circles)} уникальных окружностей.")
    
    plot_gasket(apollonian_circles, output=args.output)


if __name__ == "__main__":
    main()
