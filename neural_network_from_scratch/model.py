import numpy as np

class NeuralNetwork:
    """Multi‑layer perceptron with ReLU hidden layers and softmax output."""
    
    def __init__(self, layer_sizes, learning_rate=0.01, seed=42):
        """
        layer_sizes: list of ints, e.g. [784, 128, 64, 10]
        learning_rate: float
        """
        np.random.seed(seed)
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        
        for i in range(len(layer_sizes) - 1):
            # He initialization for ReLU
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2. / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def _relu(self, x):
        return np.maximum(0, x)
    
    def _relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def _softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        """Forward pass, returns output probabilities and caches for backprop."""
        self.cache = {}  # store intermediate values
        a = X
        self.cache['a0'] = a
        
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            z = a @ w + b
            if i < len(self.weights) - 1:  # hidden layers: ReLU
                a = self._relu(z)
            else:                           # output layer: linear (softmax later)
                a = z
            self.cache[f'z{i+1}'] = z
            self.cache[f'a{i+1}'] = a
        
        # Apply softmax to output layer for probabilities
        probs = self._softmax(a)
        return probs
    
    def backward(self, X, y, probs):
        """Backpropagation using cross‑entropy loss."""
        m = X.shape[0]  # batch size
        
        # Gradient of loss w.r.t. output logits (softmax + cross‑entropy)
        dlogits = probs.copy()
        dlogits[range(m), y] -= 1
        dlogits /= m
        
        grads_w = []
        grads_b = []
        
        # Backprop through layers in reverse
        for i in reversed(range(len(self.weights))):
            a_prev = self.cache[f'a{i}']  # activation of previous layer
            z = self.cache[f'z{i+1}']
            
            # Gradient for current layer weights and biases
            dw = a_prev.T @ dlogits
            db = np.sum(dlogits, axis=0, keepdims=True)
            grads_w.insert(0, dw)
            grads_b.insert(0, db)
            
            if i > 0:  # propagate gradient to previous layer
                dlogits = dlogits @ self.weights[i].T
                # ReLU derivative
                dlogits *= self._relu_derivative(z)
        
        return grads_w, grads_b
    
    def update(self, grads_w, grads_b):
        """Gradient descent update."""
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * grads_w[i]
            self.biases[i]   -= self.learning_rate * grads_b[i]
    
    def train_step(self, X_batch, y_batch):
        """Single training step: forward, backward, update."""
        probs = self.forward(X_batch)
        grads_w, grads_b = self.backward(X_batch, y_batch, probs)
        self.update(grads_w, grads_b)
        return self._cross_entropy_loss(probs, y_batch)
    
    def _cross_entropy_loss(self, probs, y):
        m = y.shape[0]
        log_likelihood = -np.log(probs[range(m), y] + 1e-8)
        return np.sum(log_likelihood) / m
    
    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)
    
    def accuracy(self, X, y):
        preds = self.predict(X)
        return np.mean(preds == y)
