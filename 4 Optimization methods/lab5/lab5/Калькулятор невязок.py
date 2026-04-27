import numpy as np
import os
import re
from scipy.optimize import minimize
from gaussian_residues import gaussian_residues
from paraboloid_residues import paraboloid_residues
from RBF_residues import RBF_residues

np.set_printoptions(precision=4, suppress=True, linewidth=120)

path_to_variant_filenames = './варианты'

variant_filenames = [
    os.path.join(root, name)
    for root, dirs, files in os.walk(path_to_variant_filenames)
    for name in files
    if name.endswith(('.py'))
]

variant_filenames = sorted(variant_filenames)

for variant_filename in variant_filenames:
    # имя файла с заготовкой для студента (конкретный вариант)
    data = None # данные по варианту будут извлечены из файла .py
    
    try:
        with open(variant_filename, 'r',encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1): 
                if 'data = np.array([' in line:
                    strs = ''.join([file.readline().strip() for idx in range(5)])
                    data = eval('np.array(['+strs+'])')
                    break
    except Exception as e:
        print(f"An error occurred for {variant_filename}. {e}")
    
    print("="*70)
    variant_int = re.findall(r'\d+', variant_filename)[0]
    print(f"VARIANT: {variant_int}")
    print("="*70)
    if not(data is None):
        gaussian_residues(data)
        paraboloid_residues(data)
        RBF_residues(data)
