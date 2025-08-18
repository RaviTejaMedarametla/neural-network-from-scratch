import numpy as np
import pandas as pd

# Custom uniform initialization function for weights and biases
def custom_uniform(n_in, n_out, scale_factor=0.1):
    """Custom uniform function that scales the Xavier limits for weight initialization."""
    limit = np.sqrt(6 / (n_in + n_out)) * scale_factor
    return np.random.uniform(-limit, limit, (n_in, n_out))

# ReLU activation function
def relu(x):
    return np.maximum(0, x)

# Softmax function to output probabilities
def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

# Two-layer neural network class
class TwoLayerNeural():
    def __init__(self, n_features, n_classes):
        # Initialize weights and biases using custom_uniform
        self.weights1 = custom_uniform(n_features, 64, scale_factor=0.5)  # Weights from input to hidden layer (64 neurons)
        self.bias1 = np.zeros((1, 64))  # Bias for hidden layer

        self.weights2 = custom_uniform(64, n_classes, scale_factor=0.5)  # Weights from hidden to output layer (10 classes)
        self.bias2 = np.zeros((1, n_classes))  # Bias for output layer

    def forward(self, X):
        # Hidden Layer: Z1 = XW1 + B1, A1 = relu(Z1)
        self.Z1 = np.dot(X, self.weights1) + self.bias1
        self.A1 = relu(self.Z1)

        # Output Layer: Z2 = A1W2 + B2, A2 = softmax(Z2)
        self.Z2 = np.dot(self.A1, self.weights2) + self.bias2
        self.A2 = softmax(self.Z2)

        return self.A2

# Main execution block
if __name__ == '__main__':
    # Paths to your train and test files (replace these with actual paths)
    train_file_path = "C:/Users/ravit/PycharmProjects/Neural Network from Scratch/Neural Network from Scratch/Data/fashion-mnist_train.csv"
    test_file_path = "C:/Users/ravit/PycharmProjects/Neural Network from Scratch/Neural Network from Scratch/Data/fashion-mnist_test.csv"

    # Read the train and test data
    raw_train = pd.read_csv(train_file_path)
    raw_test = pd.read_csv(test_file_path)

    # Extract features and labels
    X_train = raw_train[raw_train.columns[1:]].values  # Features from the training dataset
    X_test = raw_test[raw_test.columns[1:]].values    # Features from the test dataset

    y_train = raw_train['label'].values  # Labels from the training dataset
    y_test = raw_test['label'].values    # Labels from the test dataset

    # Normalize data between 0 and 1
    X_train_scaled = X_train / 255.0
    X_test_scaled = X_test / 255.0

    # Create an instance of the TwoLayerNeural class
    model = TwoLayerNeural(n_features=X_train_scaled.shape[1], n_classes=10)

    # Perform a forward pass for the first two items of the training data
    forward_output = model.forward(X_train_scaled[:2])

    # Flatten the 2D output into a single 1D list of floats
    forward_output_flattened = forward_output.flatten()

    # Convert np.float64 to plain float and round to 4 decimal places, then print
    print([round(float(val), 4) for val in forward_output_flattened])
