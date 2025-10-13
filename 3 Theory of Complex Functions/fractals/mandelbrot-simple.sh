 #!/bin/bash

# Создаем временную директорию для картинок
mkdir -p temp

# Генерируем последовательность изображений
for n in {0..100}; do
    echo "Генерация кадра $n..."
    python 1_mandelbrot.py --max_iter $n --output "temp/mandelbrot-${n}.png"
done

# Создаем GIF с помощью ffmpeg
echo "Создание GIF..."
ffmpeg -framerate 10 -i temp/mandelbrot-%d.png -vf "scale=640:-1:flags=lanczos" -c:v gif mandelbrot_animation.gif

# Очищаем временные файлы (опционально)
# rm -rf temp

echo "Готово! Анимация сохранена как mandelbrot_animation.gif"
