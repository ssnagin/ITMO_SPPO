import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

# ==============================================================================
# ВАРИАНТ 4
# ==============================================================================
data = np.array([
    [0.79, 0.95, 0.51],
    [2.02, 1.90, 3.31],
    [2.95, 2.95, 5.97],
    [4.14, 4.10, 1.94],
    [4.89, 5.16, 0.37]
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
    print(f"  Точка {i}: x={X[i]:.2f}, y={Y[i]:.2f}, z={Z[i]:.2f}")

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
print(f"  Amplitude (A):     {A_start:.2f}")
print(f"  Center (x0, y0):   ({x0_start:.2f}, {y0_start:.2f})")
print(f"  Sigma_x:           {sigma_x_start:.2f}")
print(f"  Sigma_y:           {sigma_y_start:.2f}")
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

print("\nЗапускаем оптимизацию...")
result = minimize(loss_function, params_start, method='L-BFGS-B', bounds=bounds)

# ==============================================================================
# РЕЗУЛЬТАТЫ
# ==============================================================================
A_opt, x0_opt, y0_opt, sigma_x_opt, sigma_y_opt, theta_opt, offset_opt = result.x

print("\n" + "="*50)
print("РЕЗУЛЬТАТЫ")
print("="*50)
print(f"\nA = {A_opt:.4f}")
print(f"x0 = {x0_opt:.4f}, y0 = {y0_opt:.4f}")
print(f"sigma_x = {sigma_x_opt:.4f}, sigma_y = {sigma_y_opt:.4f}")
print(f"theta = {theta_opt:.2f} рад = {np.degrees(theta_opt):.2f}°, offset = {offset_opt:.4f}")
print(f"\nФинальная ошибка: {result.fun:.8f}")

# ==============================================================================
# ЗАДАНИЕ 6: Проверка
# ==============================================================================
predictions = []
for i in range(len(X)):
    pred = ................  
    predictions.append(pred)

print("\nПроверка:")
for i in range(len(X)):
    print(f"Точка {i}: z={Z[i]:.2f}, предсказание модели={predictions[i]:.2f}")

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
print("\n✅ Готово! Получилась двумерная гауссиана - аппроксимация для z(x,y)!")
plt.savefig('model_plot.png', dpi=300)
plt.show()
