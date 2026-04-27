import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=4, suppress=True, linewidth=120)


class KMeansScratch:
    """K-Means clustering algorithm implemented from scratch using numpy."""
    def __init__(self, n_clusters=2, max_iters=100):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.centroids = None
    
    def _euclidean_distance(self, X, centroids):
        """Compute Euclidean distance between X and centroids."""
        # X: (N, 2), Centroids: (K, 2)
        # Returns: (N, K)
        distances = np.zeros((X.shape[0], centroids.shape[0]))
        for k in range(centroids.shape[0]):
            diff = X - centroids[k]
            distances[:, k] = np.sqrt(np.sum(diff ** 2, axis=1))
        return distances
    
    def fit(self, X):
        """Fit K-Means to data X."""        
        # Initialize centroids randomly from data points
        indices = np.array([0,2])#np.random.choice(X.shape[0], self.n_clusters, replace=False)
        self.centroids = X[indices].copy()
        
        for i in range(self.max_iters):
            # 1. Assign clusters
            distances = self._euclidean_distance(X, self.centroids)
            labels = np.argmin(distances, axis=1)
            
            # 2. Update centroids
            new_centroids = np.zeros_like(self.centroids)
            for k in range(self.n_clusters):
                cluster_points = X[labels == k]
                if len(cluster_points) > 0:
                    new_centroids[k] = cluster_points.mean(axis=0)
                else:
                    new_centroids[k] = self.centroids[k]
            
            # Check convergence
            shift = np.sqrt(np.sum((new_centroids - self.centroids) ** 2))
            self.centroids = new_centroids
            
            if shift < 1e-4:
                #print("K-Means Converged.")
                break
        return self.centroids

class RBFNetwork:
    """RBF Neural Network with Gradient Descent for all parameters."""
    def __init__(self, n_hidden=2, lr=0.01, epochs=500):
        self.n_hidden = n_hidden
        self.lr = lr
        self.epochs = epochs
        self.centers = None
        self.widths = None
        self.weights = None
        self.bias = None
        self.history = []
    
    def _gaussian(self, X, center, width):
        """Calculate Gaussian RBF activation."""
        diff = X - center
        dist_sq = np.sum(diff ** 2, axis=1)
        return np.exp(-dist_sq / (2 * width ** 2))
    
    def initialize(self, X):
        """Initialize centers using K-Means, widths using heuristic, weights randomly."""
        kmeans = KMeansScratch(n_clusters=self.n_hidden)
        self.centers = kmeans.fit(X)
        
        # Initialize widths: average distance between centers
        dist_between_centers = np.sqrt(np.sum((self.centers[0] - self.centers[1])**2))
        self.widths = np.array([dist_between_centers, dist_between_centers]) * 0.5
        self.widths = np.maximum(self.widths, 0.1) # Prevent division by zero
        
        # Initialize weights and bias
        self.weights = np.random.randn(self.n_hidden) * 0.5
        self.bias = 0.0        

    def forward(self, X):
        """Forward pass."""
        activations = np.zeros((X.shape[0], self.n_hidden))
        for j in range(self.n_hidden):
            activations[:, j] = self._gaussian(X, self.centers[j], self.widths[j])
        output = np.dot(activations, self.weights) + self.bias
        return output, activations
    
    def train(self, X, y):
        """Train using Gradient Descent."""        
        N = X.shape[0]
        
        for epoch in range(self.epochs):
            # 1. Forward Pass
            y_pred, activations = self.forward(X)
            error = y_pred - y
            loss = np.mean(error ** 2)
            
            # Record history
            if epoch < 5 or epoch % 100 == 0 or epoch == self.epochs - 1:
                self.history.append({
                    'epoch': epoch,
                    'loss': loss,
                    'centers': self.centers.copy(),
                    'widths': self.widths.copy(),
                    'weights': self.weights.copy(),
                    'bias': self.bias
                })
            
            # 2. Backward Pass (Gradients)
            grad_w = np.zeros(self.n_hidden)
            grad_b = 0.0
            grad_sigma = np.zeros(self.n_hidden)
            grad_c = np.zeros_like(self.centers)
            
            # Calculate gradients summing over all samples
            for i in range(N):
                for j in range(self.n_hidden):
                    phi = activations[i, j]
                    diff = X[i] - self.centers[j]
                    dist_sq = np.sum(diff ** 2)
                    
                    # Gradient for weights
                    grad_w[j] += (2.0 / N) * error[i] * phi
                    
                    # Gradient for bias
                    grad_b += (2.0 / N) * error[i]
                    
                    # Gradient for widths (sigma)
                    # d/d_sigma exp(-d^2 / 2s^2) = exp(...) * (d^2 / s^3)
                    if self.widths[j] > 1e-5:
                        grad_sigma[j] += (2.0 / N) * error[i] * self.weights[j] * phi * (dist_sq / (self.widths[j] ** 3))
                    
                    # Gradient for centers
                    # d/d_c exp(-||x-c||^2 / 2s^2) = exp(...) * (x-c) / s^2
                    if self.widths[j] > 1e-5:
                        grad_c[j] += (2.0 / N) * error[i] * self.weights[j] * phi * (diff / (self.widths[j] ** 2))
            
            # 3. Update Parameters
            self.weights -= self.lr * grad_w
            self.bias -= self.lr * grad_b
            self.widths -= self.lr * grad_sigma
            self.centers -= self.lr * grad_c
            
            # Constraint: widths must be positive
            self.widths = np.maximum(self.widths, 0.01)         


    def predict(self, X):
        y_pred, _ = self.forward(X)
        return y_pred

def RBF_residues(data: np.ndarray):    
        
    X = data[:,:2]  # x-coordinates: [1, 2, 3, 4, 5]
    z = data[:, 2]
  
    # Set random seed for reproducibility
    np.random.seed(42)

    model = RBFNetwork(n_hidden=2, lr=0.1, epochs=500)
    model.initialize(X)
    model.train(X, z)
  
    z_pred = model.predict(X)
    
    errors = z_pred - z
    squared_errors = errors ** 2
    
    print(f"\nRBF-net Model: z(x,y) = {model.bias:.4f} + ")
    for i in range(model.n_hidden):
        c1, c2 = model.centers[i]
        w = model.weights[i]
        s = model.widths[i]
        print(f"    {w:.4f} * exp(-((x1-{c1:.4f})^2 + (x2-{c2:.4f})^2) / (2*{s:.4f}^2)) + ")
    print(f"{'Sample':<8} {'x':<4} {'y':<4} {'Actual':<8} {'Predicted':<10} {'Error':<8} {'SqError':<10}")
    print("-"*80)
    for i in range(len(data)):
        x_i, y_i, z_true = X[i,0], X[i,1], z[i]          
        print(f"{i:<8} {x_i:<4.2f} {y_i:<4.2f} {z_true:<8.2f} {z_pred[i]:<10.3f} {errors[i]:<8.3f} {squared_errors[i]:<10.3f}")
        
