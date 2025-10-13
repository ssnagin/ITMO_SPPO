#!/bin/bash

# Создаем временную директорию для картинок
# mkdir -p temp

# # Генерируем последовательность изображений с разными значениями c
# for n in {0..100}; do
#     # Вычисляем значение c, которое будет меняться по кругу
#     # c = r * e^(i*theta), где theta меняется от 0 до 2π
#     theta=$(echo "scale=10; $n * 2 * 3.1415926535 / 100" | bc -l)
#     real_part=$(echo "scale=10; 0.7885 * c($theta)" | bc -l)
#     imag_part=$(echo "scale=10; 0.7885 * s($theta)" | bc -l)
    
#     # Форматируем числа (bc выдает числа типа -.123, нужно 0.123)
#     real_part=$(echo $real_part | sed 's/^\-\./-0./' | sed 's/^\./0./')
#     imag_part=$(echo $imag_part | sed 's/^\-\./-0./' | sed 's/^\./0./')
    
#     c_value="${real_part}+${imag_part}j"
    
#     echo "Генерация кадра $n с c = $c_value..."
#     python 2_julia.py --c"=$c_value" --output "temp/julia-${n}.png"
# done

# Создаем GIF с помощью ffmpeg
echo "Создание GIF..."
ffmpeg -framerate 10 -i temp/julia-%d.png -vf "scale=640:-1:flags=lanczos" -c:v gif julia_c_animation.gif

# Очищаем временные файлы (опционально)
# rm -rf temp

echo "Готово! Анимация сохранена как julia_c_animation.gif"