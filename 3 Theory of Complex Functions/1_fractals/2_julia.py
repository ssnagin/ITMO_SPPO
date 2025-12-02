import numpy as np
import matplotlib.pyplot as plt
import argparse

def julia_set(h, w, c, max_iter, x_min=-2.0, x_max=2.0, y_min=-2.0, y_max=2.0):
    """
    Генерирует заполненное множество Жюлиа для функции f(z) = z^2 + c.
    
    Параметры:
    h, w       — высота и ширина изображения (пиксели)
    c          — комплексный параметр отображения
    max_iter   — максимальное число итераций
    x_min...y_max — границы области на комплексной плоскости
    
    Возвращает:
    2D массив с количеством итераций до "убегания" для каждой точки
    """
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    z = x + 1j * y
    divtime = np.full(z.shape, max_iter, dtype=int)

    for i in range(max_iter):
        mask = np.abs(z) <= 2
        if not np.any(mask):
            break
        z[mask] = z[mask]**2 + c
        escaped = mask & (np.abs(z) > 2)
        divtime[escaped] = i

    return divtime

def plot_julia(h=800, w=800, c=-0.5251993+0.5251993j, max_iter=200,
               x_min=-2.0, x_max=2.0, y_min=-2.0, y_max=2.0,
               cmap='magma', output=None):
    """
    Строит и отображает (и/или сохраняет) множество Жюлиа.
    """
    julia = julia_set(h, w, c, max_iter, x_min, x_max, y_min, y_max)
    plt.figure(figsize=(8, 8))
    plt.imshow(julia, extent=[x_min, x_max, y_min, y_max], cmap=cmap, origin='lower')
    plt.colorbar(label='Итерации до убегания')
    plt.title(f'Множество Жюлиа (c = {c}, max_iter = {max_iter})')
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    if output:
        plt.savefig(output, dpi=150, bbox_inches='tight')
        print(f"Изображение сохранено в '{output}'")
    else:
        plt.show()

def parse_complex(s):
    """Помощник для парсинга комплексного числа из строки вида 'a+bj'."""
    try:
        return complex(s.replace(' ', ''))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Неверный формат комплексного числа: {s}")

def main():
    parser = argparse.ArgumentParser(description="Визуализация множества Жюлиа для f(z) = z^2 + c")
    parser.add_argument('--c', type=parse_complex, default=-0.5251993+0.5251993j,
                        help='Комплексный параметр c (например: -0.5251993+0.5251993j)')
    parser.add_argument('--width', type=int, default=800, help='Ширина изображения (пиксели)')
    parser.add_argument('--height', type=int, default=800, help='Высота изображения (пиксели)')
    parser.add_argument('--max_iter', type=int, default=200, help='Максимальное число итераций')
    parser.add_argument('--x_min', type=float, default=-2.0, help='Левая граница по Re(z)')
    parser.add_argument('--x_max', type=float, default=2.0, help='Правая граница по Re(z)')
    parser.add_argument('--y_min', type=float, default=-2.0, help='Нижняя граница по Im(z)')
    parser.add_argument('--y_max', type=float, default=2.0, help='Верхняя граница по Im(z)')
    parser.add_argument('--cmap', type=str, default='magma', 
                        help='Цветовая палитра (например: hot, plasma, viridis, magma)')
    parser.add_argument('--output', type=str, default=None, 
                        help='Имя файла для сохранения изображения (например: julia.png)')

    args = parser.parse_args()

    plot_julia(
        h=args.height,
        w=args.width,
        c=args.c,
        max_iter=args.max_iter,
        x_min=args.x_min,
        x_max=args.x_max,
        y_min=args.y_min,
        y_max=args.y_max,
        cmap=args.cmap,
        output=args.output
    )

if __name__ == "__main__":
    main()
