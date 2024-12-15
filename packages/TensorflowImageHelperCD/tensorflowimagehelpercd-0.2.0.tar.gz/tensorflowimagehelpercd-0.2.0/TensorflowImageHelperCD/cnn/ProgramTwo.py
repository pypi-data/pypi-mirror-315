


def programTwoA():
    """
    Design a single unit perceptron for classification of a linearly separable binary dataset without using pre-defined models. Use the Perceptron from sklearn.
    """
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.linear_model import Perceptron
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt
    X, y = make_classification(
        n_samples=100, n_features=2, n_informative=2,
        n_redundant=0, n_clusters_per_class=1,
        flip_y=0, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    perceptron = Perceptron(max_iter=1000, eta0=1, random_state=42)
    perceptron.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, perceptron.predict(X_test))
    print(f'Accuracy: {accuracy * 100:.2f}%')
    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100),
        np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 100)
    )
    Z = perceptron.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', cmap='coolwarm', marker='o')
    plt.title('Perceptron Classification')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

def programTwoB():
    """
    Identify the problem with single unit Perceptron. Classify using Or, And and Xor data and analyze the result.
    """
    import numpy as np
    from sklearn.linear_model import Perceptron
    from sklearn.metrics import accuracy_score
    # Data for AND, OR, XOR gates
    data = {
        'AND': (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 0, 0, 1])),  # Use 0 and 1 for labels
        'OR': (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 1])),  # Use 0 and 1 for labels
        'XOR': (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 0])),  # Use 0 and 1 for labels
    }
    # Classify AND, OR, XOR gates
    for gate, (X, y) in data.items():
        perceptron = Perceptron(max_iter=10, eta0=1, random_state=42)
        perceptron.fit(X, y)
        y_pred = perceptron.predict(X)
        acc = accuracy_score(y, y_pred) * 100
        print(f"{gate} gate accuracy: {acc:.2f}%")
        print(f"Predictions: {y_pred}")
        print(f"True Labels: {y}")
