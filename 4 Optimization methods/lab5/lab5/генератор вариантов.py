import numpy as np
import hashlib
import os

def generate_beautiful_variant(variant_number):
    """
    Генерирует красивый вариант с 5 точками, идеально ложащимися на гауссиану
    """
    
    # Используем номер варианта как seed для детерминированной генерации
    seed = int(hashlib.md5(str(variant_number).encode()).hexdigest()[:8], 16)
    np.random.seed(seed)
    
    # Параметры настоящей гауссианы (красивые значения)
    true_params = {
        'A': np.random.uniform(4.0, 6.0),      # амплитуда
        'x0': np.random.uniform(2.5, 3.5),     # центр x
        'y0': np.random.uniform(2.5, 3.5),     # центр y
        'sigma_x': np.random.uniform(0.8, 1.5), # ширина по x
        'sigma_y': np.random.uniform(0.8, 1.5), # ширина по y
        'offset': np.random.uniform(-0.3, 0.3)  # смещение
    }
    
    # Генерируем 5 точек в разных местах
    points_x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    points_y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Добавляем небольшой шум к координатам
    noise_x = np.random.normal(0, 0.1, 5)
    noise_y = np.random.normal(0, 0.1, 5)
    points_x = points_x + noise_x
    points_y = points_y + noise_y
    
    # Вычисляем значения z по настоящей гауссиане
    def true_gaussian(x, y):
        dx = x - true_params['x0']
        dy = y - true_params['y0']
        exp_term = np.exp(-(dx**2/(2*true_params['sigma_x']**2) + 
                           dy**2/(2*true_params['sigma_y']**2)))
        return true_params['A'] * exp_term + true_params['offset']
    
    points_z = np.array([true_gaussian(x, y) for x, y in zip(points_x, points_y)])
    
    # Добавляем маленький шум к z
    noise_z = np.random.normal(0, 0.05, 5)
    points_z = points_z + noise_z
    
    # Округляем до 2 знаков для красоты
    points_x = np.round(points_x, 2)
    points_y = np.round(points_y, 2)
    points_z = np.round(points_z, 2)
    
    return points_x, points_y, points_z, true_params

def create_variant_code(variant_number):
    """Создает код для указанного варианта"""
    
    X, Y, Z, true_params = generate_beautiful_variant(variant_number)
    
    code = f'''import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

# ==============================================================================
# ВАРИАНТ {variant_number}
# ==============================================================================
data = np.array([
    [{X[0]:.2f}, {Y[0]:.2f}, {Z[0]:.2f}],
    [{X[1]:.2f}, {Y[1]:.2f}, {Z[1]:.2f}],
    [{X[2]:.2f}, {Y[2]:.2f}, {Z[2]:.2f}],
    [{X[3]:.2f}, {Y[3]:.2f}, {Z[3]:.2f}],
    [{X[4]:.2f}, {Y[4]:.2f}, {Z[4]:.2f}]
])

# ==============================================================================
# ЗАДАНИЕ 1: Извлеките значения из data (признаки X, Y, Z индексируются как столбцы data 0,1,2 соответственно)
# Подсказка: используйте слайсы (slices) для выделения подмассива из массива numpy.ndarray 
# ==============================================================================
X = ................  
Y = ................ 
Z = ................  

print("Мои данные:")
for i in range(len(X)):
    print(f"  Точка {{i}}: x={{X[i]:.2f}}, y={{Y[i]:.2f}}, z={{Z[i]:.2f}}")

# ==============================================================================
# ЗАДАНИЕ 2: Функция Гаусса
# ==============================================================================
def gauss_2d(x, y, A, x0, y0, sigma_x, sigma_y, theta=0, offset=0):
    """
    2D функция Гаусса
    Формула: A * exp(-(x_new^2/(2*sigma_x^2) + y_new^2/(2*sigma_y^2))) + offset,
    x_new, y_new - координаты в канонической системе (получена из исходной сдвигом и поворотом,
    используя параметры x0, y0, theta)
    """
    if theta != 0:
        x_new = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
        y_new = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    else:        
        x_new = ................  
        y_new = ................  
    exp_part = ................
    result = A * exp_part + offset
    return result

# ==============================================================================
# ЗАДАНИЕ 3: Функция потерь (loss-функция, функция ошибки)
# ==============================================================================
def loss_function(model_params):
    """
    Вычисляем MSE для реальных и модельных значений на объектах.    
    """
    A, x0, y0, sigma_x, sigma_y, theta, offset = ................
    
    if sigma_x <= 0 or sigma_y <= 0 or A <= 0:
        return 1e10
    
    predictions = []
    for i in range(len(X)):
        pred = ................
        predictions.append(pred)
    
    errors = ................  
    mse = 0.5*np.mean(................)
    return mse

# ==============================================================================
# ЗАДАНИЕ 4: Начальное приближение
# ==============================================================================
max_idx = ................  # индекс, соотв. максимуму Z (используйте функцию argmax)
A_start = ................ + 0.1  # значение максимума Z с произвольной корректировкой (например, 0.1)
x0_start = ................ # значение Х, соотв. max_idx (точка максимума) 
y0_start = ................ # значение Y, соотв. max_idx (точка максимума)
sigma_x_start = np.std(X) * 0.5 # std - среднеквадратичное отклонение,с.к.о., standard deviation
sigma_y_start = np.std(Y) * 0.5
offset_start = 0.0
theta_start = 0.0

params_start = [A_start, x0_start, y0_start, sigma_x_start, sigma_y_start, theta_start, offset_start]

print(f"Значения для инициализации модельных параметров (начальное приближение):")
print(f"  Amplitude (A):     {{A_start:.2f}}")
print(f"  Center (x0, y0):   ({{x0_start:.2f}}, {{y0_start:.2f}})")
print(f"  Sigma_x:           {{sigma_x_start:.2f}}")
print(f"  Sigma_y:           {{sigma_y_start:.2f}}")
print(f"  Theta (rotation):  0.00 рад")
print(f"  Offset:            0.00")
print()

# ==============================================================================
# ЗАДАНИЕ 5: Границы и оптимизация (не менять)
# ==============================================================================
bounds = [
    (0.1, 10.0), (0.0, 6.0), (0.0, 6.0),
    (0.1, 5.0), (0.1, 5.0), (-np.pi/4, np.pi/4),(-1.0, 1.0)
]

print("\\nЗапускаем оптимизацию...")
result = minimize(loss_function, params_start, method='L-BFGS-B', bounds=bounds)

# ==============================================================================
# РЕЗУЛЬТАТЫ
# ==============================================================================
A_opt, x0_opt, y0_opt, sigma_x_opt, sigma_y_opt, theta_opt, offset_opt = result.x

print("\\n" + "="*50)
print("РЕЗУЛЬТАТЫ")
print("="*50)
print(f"\\nA = {{A_opt:.4f}}")
print(f"x0 = {{x0_opt:.4f}}, y0 = {{y0_opt:.4f}}")
print(f"sigma_x = {{sigma_x_opt:.4f}}, sigma_y = {{sigma_y_opt:.4f}}")
print(f"theta = {{theta_opt:.2f}} рад = {{np.degrees(theta_opt):.2f}}°, offset = {{offset_opt:.4f}}")
print(f"\\nФинальная ошибка: {{result.fun:.8f}}")

# ==============================================================================
# ЗАДАНИЕ 6: Проверка
# ==============================================================================
predictions = []
for i in range(len(X)):
    pred = ................  
    predictions.append(pred)

print("\\nПроверка:")
for i in range(len(X)):
    print(f"Точка {{i}}: z={{Z[i]:.2f}}, предсказание модели={{predictions[i]:.2f}}")

# ==============================================================================
# ЗАДАНИЕ 7: Визуализация
# ==============================================================================
x_grid = np.linspace(0, 6, 50)
y_grid = np.linspace(0, 6, 50)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

Z_grid = np.zeros((50, 50))
for i in range(50):
    for j in range(50):
        Z_grid[i, j] = ................  # аргументы x,y для gauss_2d теперь берутся в узлах равномерной сетки

# Графики
fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', alpha=0.8)
ax1.scatter(X, Y, Z, c='red', s=50)
ax1.set_title('3D-визуализация Гауссианы')

ax2 = fig.add_subplot(122)
contour = ax2.contourf(X_grid, Y_grid, Z_grid, levels=25, cmap='viridis', alpha=0.9)
scatter = ax2.scatter(X, Y, c=Z, s=120, edgecolors='black', cmap='viridis')
ax2.contour(X_grid, Y_grid, Z_grid, levels=10, colors='white', alpha=0.3, linewidths=0.5)
ax2.set_xlabel('X', fontsize=10)
ax2.set_ylabel('Y', fontsize=10)
ax2.set_title('Линии уровня модельной функции и точки области задания исходной', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()
cbar = plt.colorbar(contour, ax=ax2, label='Z')
cbar.ax.tick_params(labelsize=9)

plt.tight_layout()
print("\\n✅ Готово! Получилась двумерная гауссиана - аппроксимация для z(x,y)!")
plt.savefig('model_plot.png', dpi=300)
plt.show()
'''

    return code, true_params

# ==============================================================================
# ГЕНЕРАТОР ВАРИАНТОВ (для обычного Python)
# ==============================================================================

print("🎓 ГЕНЕРАТОР ВАРИАНТОВ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ")
print("="*60)

for variant in range(1,31):  
    
    variant_str = str(variant) if variant > 9 else '0'+str(variant)

    # Генерируем код для выбранного варианта
    code, true_params = create_variant_code(variant)

    # Создаём папку для вариантов, если её нет
    if not os.path.exists('варианты'):
        os.makedirs('варианты')

    # Сохраняем файл с заданием для студента
    student_filename = f'варианты/вариант_{variant_str}_задание.py'
    with open(student_filename, 'w', encoding='utf-8') as f:
        f.write(code)
     
    # Создаём папку для ответов, если её нет
    if not os.path.exists('ответы'):
        os.makedirs('ответы')
    # Сохраняем файл с ответами для преподавателя
    teacher_filename = f'ответы/вариант_{variant_str}_ответы.txt'
    with open(teacher_filename, 'w', encoding='utf-8') as f:
        f.write(f"ОТВЕТЫ ДЛЯ ВАРИАНТА {variant}\n")
        f.write("="*50 + "\n\n")
        f.write("Истинные параметры гауссианы:\n")
        f.write(f"  A = {true_params['A']:.4f}\n")
        f.write(f"  x0 = {true_params['x0']:.4f}\n")
        f.write(f"  y0 = {true_params['y0']:.4f}\n")
        f.write(f"  sigma_x = {true_params['sigma_x']:.4f}\n")
        f.write(f"  sigma_y = {true_params['sigma_y']:.4f}\n")
        f.write(f"  offset = {true_params['offset']:.4f}\n\n")
        f.write("="*50 + "\n")
        f.write("Что нужно вставить в пропуски:\n")
        f.write("="*50 + "\n")
        f.write("1. X = data[:, 0]\n")
        f.write("2. Y = data[:, 1]\n")
        f.write("3. Z = data[:, 2]\n")
        f.write("4. x_new = x - x0\n")
        f.write("5. y_new = y - y0\n")
        f.write("6. exp_part = np.exp(-((x_new**2)/(2*sigma_x**2) + (y_new**2)/(2*sigma_y**2)))\n")
        f.write("7. A, x0, y0, sigma_x, sigma_y, theta, offset = model_params\n")
        f.write("8. pred = gauss_2d(X[i], Y[i], A, x0, y0, sigma_x, sigma_y, theta, offset)\n")
        f.write("9. errors = (np.array(predictions) - Z) ** 2\n")
        f.write("10. mse = 0.5*np.mean(errors)\n")
        f.write("11. max_idx = np.argmax(Z)\n")
        f.write("12. A_start = Z[max_idx] + 0.1\n")
        f.write("13. x0_start = X[max_idx]\n")
        f.write("14. y0_start = Y[max_idx]\n")
        f.write("15. pred = gauss_2d(X[i], Y[i], A_opt, x0_opt, y0_opt, sigma_x_opt, sigma_y_opt, theta_opt, offset_opt)\n")
        f.write("16. Z_grid[i, j] = gauss_2d(X_grid[i, j], Y_grid[i, j], A_opt, x0_opt, y0_opt, sigma_x_opt, sigma_y_opt, theta_opt, offset_opt)\n")

    print(f"\n✅ Файлы созданы в папке 'варианты':")
    print(f"   - {student_filename} (для студента)")
    print(f"   - {teacher_filename} (для преподавателя)")

    # Покажем данные варианта
    X, Y, Z, _ = generate_beautiful_variant(variant)
    print(f"\n📊 Данные варианта {variant}:")
    print("   x     y     z")
    print("  " + "-" * 20)
    for i in range(5):
        print(f"  {X[i]:.2f}  {Y[i]:.2f}  {Z[i]:.2f}")

    print(f"\n📁 Файлы сохранены в папке 'варианты'")
    print(f"   Откройте эту папку и возьмите нужный файл!")

    print("\n💡 Истинные параметры (для проверки):")
    print(f"  A = {true_params['A']:.4f}")
    print(f"  x0 = {true_params['x0']:.4f}, y0 = {true_params['y0']:.4f}")
    print(f"  sigma_x = {true_params['sigma_x']:.4f}, sigma_y = {true_params['sigma_y']:.4f}")
    print(f"  offset = {true_params['offset']:.4f}")
