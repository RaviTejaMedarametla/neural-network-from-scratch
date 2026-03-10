import numpy as np
from neural_network_from_scratch.model import NeuralNetwork
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import time
import tracemalloc

def load_mnist():
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='auto')
    X = X / 255.0
    y = y.astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def main():
    X_train, X_test, y_train, y_test = load_mnist()
    
    # Model: 784 -> 128 -> 64 -> 10
    nn = NeuralNetwork(layer_sizes=[784, 128, 64, 10], learning_rate=0.01)
    
    batch_size = 64
    epochs = 5
    n_samples = X_train.shape[0]
    
    tracemalloc.start()
    start_time = time.time()
    
    for epoch in range(epochs):
        # Shuffle
        indices = np.random.permutation(n_samples)
        X_shuffled = X_train[indices]
        y_shuffled = y_train[indices]
        
        epoch_loss = 0.0
        for i in range(0, n_samples, batch_size):
            X_batch = X_shuffled[i:i+batch_size]
            y_batch = y_shuffled[i:i+batch_size]
            loss = nn.train_step(X_batch, y_batch)
            epoch_loss += loss * len(X_batch)
        
        epoch_loss /= n_samples
        train_acc = nn.accuracy(X_train, y_train)
        print(f"Epoch {epoch+1}: loss={epoch_loss:.4f}, train_acc={train_acc:.4f}")
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    test_acc = nn.accuracy(X_test, y_test)
    print(f"\nTest accuracy: {test_acc*100:.2f}%")
    print(f"Training time: {end_time - start_time:.2f} seconds")
    print(f"Peak memory: {peak / 1024**2:.2f} MB")

if __name__ == "__main__":
    main()
