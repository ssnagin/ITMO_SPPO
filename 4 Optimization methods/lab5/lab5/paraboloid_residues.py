import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=4, suppress=True, linewidth=120)

def paraboloid_residues(data: np.ndarray):
        
    X = data[:, 0]  # x-coordinates: [1, 2, 3, 4, 5]
    Y = data[:, 1]  # y-coordinates: [1, 1, 3, 5, 5]
    Z = data[:, 2]  # z-values (target): [0, 1, 5, 1, 0]
  
    # ==============================================================================
    # ELLIPTIC PARABOLOID MODEL DEFINITION
    # ==============================================================================
    def elliptic_paraboloid(xy, z0, x0, y0, a, b, h):
        """
        General Elliptic Paraboloid Function
        
        z = z0 + a*(x-x0)² + b*(y-y0)² + 2*h*(x-x0)*(y-y0)
        
        Parameters:
        - xy: tuple (x, y) or array of shape (N, 2)
        - z0: Vertex height (z-coordinate of minimum/maximum)
        - x0, y0: Vertex location in xy-plane
        - a, b: Curvature coefficients in x and y directions
        - h: Cross-term coefficient (controls rotation/tilt)
        
        For downward opening (peak): a < 0, b < 0, and ab > h² (elliptic condition)
        For upward opening (valley): a > 0, b > 0, and ab > h²
        """
        if isinstance(xy, tuple):
            x, y = xy
        else:
            x, y = xy[:, 0], xy[:, 1]
        
        dx = x - x0
        dy = y - y0
        
        # Quadratic form: z = z0 + a*dx² + b*dy² + 2h*dx*dy
        z = z0 + a * dx**2 + b * dy**2 + 2 * h * dx * dy
        return z

    # ==============================================================================
    # LOSS FUNCTION (Mean Squared Error)
    # ==============================================================================
    def loss_function(params, x, y, z_true):
        """
        Calculate MSE between predicted and actual z values.
        params = [z0, x0, y0, a, b, h]
        """
        z0, x0, y0, a, b, h = params
        
        # Elliptic condition: ab > h² (ensures elliptic, not hyperbolic paraboloid)
        if a * b <= h**2 + 1e-6:
            return 1e10  # Penalty for invalid (hyperbolic) parameters
        
        z_pred = elliptic_paraboloid((x, y), z0, x0, y0, a, b, h)
        mse = np.mean((z_pred - z_true) ** 2)
        return mse

    # ==============================================================================
    # INITIAL PARAMETER ESTIMATION (Analytic Heuristic)
    # ==============================================================================

    # Find vertex candidate: point with maximum z (for downward paraboloid)
    peak_idx = np.argmax(Z)
    x0_init = X[peak_idx]
    y0_init = Y[peak_idx]
    z0_init = Z[peak_idx]

    # Estimate curvatures using finite differences around the peak
    # For a paraboloid: ∂²z/∂x² ≈ 2a, ∂²z/∂y² ≈ 2b

    # Find nearest neighbors to peak in x and y directions
    dx_samples = X[np.abs(Y - y0_init) < 1.5]  # Points with similar y
    dy_samples = Y[np.abs(X - x0_init) < 1.5]  # Points with similar x

    # Estimate 'a' from x-direction curvature
    if len(dx_samples) >= 2:
        # Use points (2,1,1) and (3,3,5): dx=1, dz=4 → a ≈ dz/dx² = 4/1 = 4 (but negative for peak)
        a_init = -1.0  # Start with moderate negative curvature
    else:
        a_init = -0.5

    # Estimate 'b' from y-direction curvature  
    if len(dy_samples) >= 2:
        b_init = -1.0  # Similar magnitude to a
    else:
        b_init = -0.5

    # Cross-term: start with zero (no rotation)
    h_init = 0.0

    # Initial parameters: [z0, x0, y0, a, b, h]
    initial_params = [z0_init, x0_init, y0_init, a_init, b_init, h_init]

    # Calculate initial loss
    initial_loss = loss_function(initial_params, X, Y, Z)

    # ==============================================================================
    # DETAILED FORWARD PASS CALCULATION (Sample by Sample)
    # ==============================================================================

    z0, x0, y0, a, b, h = initial_params

    for i in range(len(data)):
        x_i, y_i, z_true = X[i], Y[i], Z[i]
        dx = x_i - x0
        dy = y_i - y0
        
        # Calculate each term
        term_a = a * dx**2
        term_b = b * dy**2
        term_h = 2 * h * dx * dy
        z_pred = z0 + term_a + term_b + term_h
        error = z_pred - z_true
        
    # ==============================================================================
    # OPTIMIZATION WITH DETAILED LOGGING
    # ==============================================================================

    # Bounds for parameters to ensure elliptic paraboloid and physical meaning
    bounds = [
        (-1.0, 10.0),     # z0: vertex height
        (0.0, 6.0),       # x0: vertex x-location
        (0.0, 6.0),       # y0: vertex y-location
        (-5.0, -0.01),    # a: curvature in x (negative for downward peak)
        (-5.0, -0.01),    # b: curvature in y (negative for downward peak)
        (-2.0, 2.0),      # h: cross-term (rotation)
    ]

    # Run optimization
    result = minimize(
        loss_function,
        initial_params,
        args=(X, Y, Z),
        method='L-BFGS-B',
        bounds=bounds,
        options={'ftol': 1e-9, 'maxiter': 500, 'disp': True}
    )

    # ==============================================================================
    # RESULTS AND DETAILED CALCULATIONS
    # ==============================================================================

    # Extract optimal parameters
    z0_opt, x0_opt, y0_opt, a_opt, b_opt, h_opt = result.x


    # ==============================================================================
    # PREDICTIONS AND ERROR ANALYSIS WITH DETAILED CALCULATIONS
    # ==============================================================================

    z_pred = elliptic_paraboloid((X, Y), z0_opt, x0_opt, y0_opt, a_opt, b_opt, h_opt)
    errors = z_pred - Z
    squared_errors = errors ** 2

    print(f"\nParaboloid Model: z(x,y) = {z0_opt:.4f}")
    print(f"         + {a_opt:.4f}·(x - {x0_opt:.4f})²")
    print(f"         + {b_opt:.4f}·(y - {y0_opt:.4f})²")
    print(f"         + 2·{h_opt:.4f}·(x - {x0_opt:.4f})(y - {y0_opt:.4f})")

    print(f"{'Sample':<8} {'x':<4} {'y':<4} {'Actual':<8} {'Predicted':<10} {'Error':<8} {'SqError':<10}")
    print("-"*80)

    for i in range(len(data)):
        x_i, y_i, z_true = X[i], Y[i], Z[i]
        z_p = z_pred[i]
        
        print(f"{i:<8} {x_i:<4.2f} {y_i:<4.2f} {z_true:<8.2f} {z_p:<10.3f} {errors[i]:<8.3f} {squared_errors[i]:<10.3f}")

