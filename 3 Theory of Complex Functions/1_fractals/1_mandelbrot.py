import numpy as np
import matplotlib.pyplot as plt
import argparse

def mandelbrot(h, w, max_iter, x_min=-2.0, x_max=1.0, y_min=-1.5, y_max=1.5):
    """
    Генерирует изображение множества Мандельброта.
    
    Параметры:
    h, w       — высота и ширина изображения в пикселях
    max_iter   — максимальное число итераций
    x_min...y_max — границы прямоугольника на комплексной плоскости
    
    Возвращает:
    2D массив с количеством итераций до "убегания" для каждой точки
    """
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    c = x + 1j * y
    z = np.zeros_like(c)
    divtime = np.full(z.shape, max_iter, dtype=int)

    for i in range(max_iter):
        mask = np.abs(z) <= 2
        if not np.any(mask):
            break
        z[mask] = z[mask]**2 + c[mask]
        escaped = mask & (np.abs(z) > 2)
        divtime[escaped] = i

    return divtime

def plot_mandelbrot(h=800, w=1000, max_iter=100, x_min=-2.0, x_max=1.0,
                    y_min=-1.5, y_max=1.5, cmap='magma', output=None):
    """
    Строит и отображает (и/или сохраняет) множество Мандельброта.
    """
    mandel = mandelbrot(h, w, max_iter, x_min, x_max, y_min, y_max)
    plt.figure(figsize=(12, 8))
    plt.imshow(mandel, extent=[x_min, x_max, y_min, y_max], cmap=cmap, origin='lower')
    plt.colorbar(label='Итерации до убегания')
    plt.title(f'Множество Мандельброта (max_iter={max_iter})')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    if output:
        plt.savefig(output, dpi=150, bbox_inches='tight')
        print(f"Изображение сохранено в '{output}'")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Визуализация множества Мандельброта")
    parser.add_argument('--width', type=int, default=1000, help='Ширина изображения (в пикселях)')
    parser.add_argument('--height', type=int, default=800, help='Высота изображения (в пикселях)')
    parser.add_argument('--max_iter', type=int, default=200, help='Максимальное число итераций')
    parser.add_argument('--x_min', type=float, default=-2.0, help='Левая граница по Re(c)')
    parser.add_argument('--x_max', type=float, default=1.0, help='Правая граница по Re(c)')
    parser.add_argument('--y_min', type=float, default=-1.5, help='Нижняя граница по Im(c)')
    parser.add_argument('--y_max', type=float, default=1.5, help='Верхняя граница по Im(c)')
    parser.add_argument('--cmap', type=str, default='magma', help='Цветовая палитра (например: hot, plasma, viridis, magma)')
    parser.add_argument('--output', type=str, default=None, help='Имя файла для сохранения изображения (например: mandel.png)')

    args = parser.parse_args()

    plot_mandelbrot(
        h=args.height,
        w=args.width,
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
