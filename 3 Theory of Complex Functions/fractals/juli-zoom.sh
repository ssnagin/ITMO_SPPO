#!/bin/bash

# Создаем временную директорию для кадров
mkdir -p temp

# Параметры зума для множества Жюлиа
START_X_MIN=-1.5
START_X_MAX=1.5
START_Y_MIN=-1.5
START_Y_MAX=1.5
ZOOM_FACTOR=0.95  # Коэффициент зума (меньше 1 = увеличение)
FRAMES=100
C_PARAM="-0.5251993+0.5251993j"  # Красивый параметр из задания

echo "Создание анимации зума множества Жюлиа (c = $C_PARAM)..."
echo "Кадров: $FRAMES"

# Проверяем наличие bc
if ! command -v bc &> /dev/null; then
    echo "Ошибка: bc не установлен. Установите: sudo apt install bc"
    exit 1
fi

# Вычисляем центр области
CENTER_X=$(echo "scale=10; ($START_X_MIN + $START_X_MAX) / 2" | bc)
CENTER_Y=$(echo "scale=10; ($START_Y_MIN + $START_Y_MAX) / 2" | bc)

echo "Центр: ($CENTER_X, $CENTER_Y)"

# Начальные размеры области
WIDTH=$(echo "scale=10; $START_X_MAX - $START_X_MIN" | bc)
HEIGHT=$(echo "scale=10; $START_Y_MAX - $START_Y_MIN" | bc)

for ((n=0; n<FRAMES; n++)); do
    # Вычисляем текущие границы с учетом зума
    CURRENT_WIDTH=$(echo "scale=10; $WIDTH * ($ZOOM_FACTOR ^ $n)" | bc)
    CURRENT_HEIGHT=$(echo "scale=10; $HEIGHT * ($ZOOM_FACTOR ^ $n)" | bc)
    
    CURRENT_X_MIN=$(echo "scale=10; $CENTER_X - $CURRENT_WIDTH / 2" | bc)
    CURRENT_X_MAX=$(echo "scale=10; $CENTER_X + $CURRENT_WIDTH / 2" | bc)
    CURRENT_Y_MIN=$(echo "scale=10; $CENTER_Y - $CURRENT_HEIGHT / 2" | bc)
    CURRENT_Y_MAX=$(echo "scale=10; $CENTER_Y + $CURRENT_HEIGHT / 2" | bc)
    
    printf "\rГенерация кадра %d/%d" $((n+1)) $FRAMES
    
    python 2_julia.py \
        --c "$C_PARAM" \
        --max_iter 100 \
        --x_min $CURRENT_X_MIN \
        --x_max $CURRENT_X_MAX \
        --y_min $CURRENT_Y_MIN \
        --y_max $CURRENT_Y_MAX \
        --output "temp/julia_zoom_$(printf "%03d" $n).png" > /dev/null 2>&1
done

echo ""
echo "Создание GIF анимации..."

# Создаем GIF с помощью ffmpeg
ffmpeg -y \
    -framerate 15 \
    -i temp/julia_zoom_%03d.png \
    -vf "scale=800:-1:flags=lanczos" \
    -loop 0 \
    julia_zoom.gif

echo "Анимация готова: julia_zoom.gif"
