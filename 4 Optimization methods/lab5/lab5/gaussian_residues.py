import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=4, suppress=True, linewidth=120)

def gaussian_residues(data: np.ndarray):
    
    X = data[:, 0] 
    Y = data[:, 1] 
    Z = data[:, 2]  

    # ==============================================================================
    # 2D GAUSSIAN FUNCTION DEFINITION
    # ==============================================================================
    def gaussian_2d(xy, A, x0, y0, sigma_x, sigma_y, theta=0, offset=0):
        """
        2D Gaussian Function (with optional rotation and offset)
        
        z = A * exp(-Q) + offset
        
        Where Q is the quadratic form:
        Q = a*(x-x0)^2 + 2*b*(x-x0)*(y-y0) + c*(y-y0)^2
        
        Parameters:
        - xy: tuple (x, y) or array of shape (N, 2)
        - A: Amplitude (peak height)
        - x0, y0: Center coordinates
        - sigma_x, sigma_y: Standard deviations
        - theta: Rotation angle in radians (optional)
        - offset: Vertical offset (baseline)
        """
        if isinstance(xy, tuple):
            x, y = xy
        else:
            x, y = xy[:, 0], xy[:, 1]
        
        # Rotate coordinates if theta != 0
        if theta != 0:
            dx = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
            dy = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
        else:
            dx = x - x0
            dy = y - y0
        
        # Quadratic form (non-rotated case simplified)
        Q = (dx**2) / (2 * sigma_x**2) + (dy**2) / (2 * sigma_y**2)
        
        return A * np.exp(-Q) + offset

    # ==============================================================================
    # LOSS FUNCTION (Mean Squared Error)
    # ==============================================================================
    def loss_function(params, x, y, z_true):
        """
        Calculate MSE between predicted and actual z values.
        params = [A, x0, y0, sigma_x, sigma_y, theta, offset]
        """
        A, x0, y0, sigma_x, sigma_y, theta, offset = params
        
        # Ensure positive sigmas and amplitude
        if sigma_x <= 0 or sigma_y <= 0 or A <= 0:
            return 1e10  # Penalty for invalid parameters
        
        z_pred = gaussian_2d((x, y), A, x0, y0, sigma_x, sigma_y, theta, offset)
        mse = np.mean((z_pred - z_true) ** 2)
        return mse

    # ==============================================================================
    # INITIAL PARAMETER ESTIMATION (Heuristic)
    # ==============================================================================

    # Find peak (maximum z) for initial center guess
    peak_idx = np.argmax(Z)
    x0_init = X[peak_idx]
    y0_init = Y[peak_idx]
    A_init = Z[peak_idx] + 0.1  # Slightly above max to allow fitting

    # Estimate sigma from data spread
    sigma_x_init = np.std(X) * 0.5
    sigma_y_init = np.std(Y) * 0.5

    # Initial parameters: [A, x0, y0, sigma_x, sigma_y, theta, offset]
    initial_params = [A_init, x0_init, y0_init, sigma_x_init, sigma_y_init, 0.0, 0.0]

    # Calculate initial loss
    initial_loss = loss_function(initial_params, X, Y, Z)

    # Bounds for parameters to ensure physical meaning
    bounds = [
        (0.1, 10.0),      # A: amplitude
        (0.0, 6.0),       # x0: center x
        (0.0, 6.0),       # y0: center y
        (0.1, 5.0),       # sigma_x
        (0.1, 5.0),       # sigma_y
        (-np.pi/4, np.pi/4),  # theta: rotation
        (-1.0, 1.0)       # offset
    ]

    # Run optimization
    result = minimize(
        loss_function,
        initial_params,
        args=(X, Y, Z),
        method='L-BFGS-B',
        bounds=bounds,
        options={'maxiter': 200}
    )

    # Extract optimal parameters
    A_opt, x0_opt, y0_opt, sx_opt, sy_opt, theta_opt, offset_opt = result.x

    # ==============================================================================
    # PREDICTIONS AND ERROR ANALYSIS
    # ==============================================================================
    
    z_pred = gaussian_2d((X, Y), *result.x)
    errors = z_pred - Z
    squared_errors = errors ** 2
    print(f"\nGaussian Model: z(x,y) = {A_opt:.4f} * exp(-Q) + {offset_opt:.4f}")
    print(f"Where Q = (x - {x0_opt:.4f})² / (2 * {sx_opt:.4f}²) + (y - {y0_opt:.4f})² / (2 * {sy_opt:.4f}²)")

    if abs(theta_opt) > 0.01:
        print(f"\nWith rotation: θ = {np.degrees(theta_opt):.2f}°")
        print("Note: Coordinates are rotated before applying the Gaussian")
    print(f"{'Sample':<8} {'x':<4} {'y':<4} {'Actual':<8} {'Predicted':<10} {'Error':<8} {'SqError':<10}")
    print("-"*50)
    for i in range(len(data)):
        print(f"{i:<8} {X[i]:<4.2f} {Y[i]:<4.2f} {Z[i]:<8.2f} {z_pred[i]:<10.3f} {errors[i]:<8.3f} {squared_errors[i]:<10.3f}")

   
