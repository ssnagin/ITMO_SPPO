 #!/bin/bash

# Создаем временную директорию для картинок
mkdir -p temp

# Генерируем последовательность изображений
for n in {0..100}; do
    echo "Генерация кадра $n..."
    python 2_julia.py --max_iter $n --output "temp/julia-${n}.png"
done

# Создаем GIF с помощью ffmpeg
echo "Создание GIF..."
ffmpeg -framerate 10 -i temp/julia-%d.png -vf "scale=640:-1:flags=lanczos" -c:v gif julia_animation.gif

# Очищаем временные файлы (опционально)
# rm -rf temp

echo "Готово! Анимация сохранена как julia_animation.gif"
