

def add(a:int , b:int) -> int:
    return a+b

def requiredPackages():
    print("tensorflow matplotlib keras tensorflow_datasets")
    print("pip install tensorflow matplotlib keras tensorflow_datasets")

def programOne():
    """
    Write a program to demonstrate the working of different activation functions like Sigmoid, Tanh, RELU and softmax to train neural network.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / np.sum(e_x, axis=0)

    x = np.linspace(-10, 10, 400)
    y = {
        'sigmoid': 1 / (1 + np.exp(-x)),
        'tanh': np.tanh(x),
        'relu': np.maximum(0, x),
        'softmax': softmax(np.array([x, x * 0.5, x * 0.2])).T
    }
    plt.figure(figsize=(12, 8))
    titles = ["Sigmoid", "Tanh", "ReLU", "Softmax"]
    colors = ['blue', 'orange', 'green']
    markers = ['-', '--', '-.']
    for i, (key, y_values) in enumerate(y.items()):
        plt.subplot(2, 2, i + 1)
        if key == 'softmax':
            for j in range(y_values.shape[1]):
                plt.plot(x, y_values[:, j], label=f"Set {j + 1}", linestyle=markers[j])
        else:
            plt.plot(x, y_values, label=key, color=colors[i])
        plt.title(f"{titles[i]} Activation Function")
        plt.xlabel("Input")
        plt.ylabel("Output")
        plt.grid(True)
        plt.legend()
    plt.tight_layout()
    plt.show()

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

def programThree():
    """
    build a Deep Feed Forward ANN by implementing the Backpropagation algorithm and test the same using appropriate data sets. Use the
number of hidden layers >= 4.
    """
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    # Load and preprocess the dataset
    X, y = load_iris(return_X_y=True)
    X = StandardScaler().fit_transform(X)
    y = tf.keras.utils.to_categorical(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # Build the model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(3, activation='softmax')
    ])
    # Compile and train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=8, validation_split=0.2, verbose=1)
    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Accuracy: {accuracy * 100:.2f}%\n Loss:{loss:.4f}')


def programFour():
    """
    Design and implement a CNN model (with 4+ layers of convolutions) to classify multi category image datasets. Use the concept of
regularization and dropout while designing the CNN model. Use the Fashion MNIST datasets. Record the Training accuracy and Test accuracy
corresponding to the following architectures:
1. Base Model
2. Model with L1 Regularization
3. Model with L2 Regularization
4. Model with Dropout
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models
    from tensorflow.keras.datasets import fashion_mnist
    from tensorflow.keras.regularizers import l1, l2
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_images, test_images = train_images[..., None] / 255.0, test_images[..., None] / 255.0

    # Function to build and evaluate a model
    def build_and_evaluate(name, regularizer=None, dropout_rate=None):
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1), kernel_regularizer=regularizer),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizer),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=regularizer),
            layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=regularizer),
            layers.Flatten(),
            layers.Dense(128, activation='relu', kernel_regularizer=regularizer),
            layers.Dense(10, activation='softmax')
        ])
        if dropout_rate:
            model.add(layers.Dropout(dropout_rate))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_split=0.2, verbose=1)
        loss, accuracy = model.evaluate(test_images, test_labels)
        print(f'Test Accuracy: {accuracy * 100:.2f}%\n Loss:{loss:.2f}')
    build_and_evaluate("Base Model")
    build_and_evaluate("L1 Regularization", regularizer=l1(0.001))
    build_and_evaluate("L2 Regularization", regularizer=l2(0.001))
    build_and_evaluate("Dropout", dropout_rate=0.5)

def programFive():
    """
    Design and implement an Image classification model to classify a dataset of images using Deep Feed Forward Neural Network. Record t
accuracy corresponding to the number of epochs. Use the MNIST datasets.
    """
    import tensorflow as tf
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Flatten
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train, X_test = X_train / 255.0, X_test / 255.0
    model = Sequential([
        Flatten(input_shape=(28, 28)),
        Dense(128, activation='relu'),
        Dense(256, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.2, verbose=1)
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Loss: {loss:.4f}')
    print(f'Test Accuracy: {accuracy * 100:.2f}%')


def programSix():
    """
    Implement Bidirectional LSTM for sentimental analysis on movie reviews.
    """
    import tensorflow as tf
    from tensorflow.keras.datasets import imdb
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=20000)
    x_train, x_test = pad_sequences(x_train, maxlen=200), pad_sequences(x_test, maxlen=200)
    model = Sequential([
        Embedding(20000, 256, input_length=200),
        Bidirectional(LSTM(256, return_sequences=True)),
        Dropout(0.5),
        Bidirectional(LSTM(128)),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
    loss, accuracy = model.evaluate(x_test, y_test)
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")


def programSeven():
    """
    Implement the standard VGG-16 & 19 CNN architecture model to classify multi category image dataset and check the accuracy
    """
    import tensorflow as tf
    from tensorflow.keras.applications import VGG16, VGG19
    from tensorflow.keras import layers, models
    import tensorflow_datasets as tfds
    def preprocess_image(image, label):
        image = tf.image.resize(image, (224, 224)) / 255.0
        return image, tf.one_hot(label, depth=5)

    (ds_train, ds_test), ds_info = tfds.load(
        'tf_flowers',
        split=['train[:80%]', 'train[80%:]'],
        as_supervised=True,
        with_info=True
    )
    ds_train = ds_train.map(preprocess_image).batch(32).prefetch(tf.data.AUTOTUNE)
    ds_test = ds_test.map(preprocess_image).batch(32).prefetch(tf.data.AUTOTUNE)

    def create_vgg_model(vgg_model_class):
        base_model = vgg_model_class(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False
        return models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(5, activation='softmax')
        ])

    def train_and_evaluate(model_class, model_name):
        print(f"Using {model_name}:")
        model = create_vgg_model(model_class)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(ds_train, validation_data=ds_test, epochs=10)
        loss, acc = model.evaluate(ds_test)
        print(f"{model_name} Accuracy: {acc:.2f}%")
    train_and_evaluate(VGG16, "VGG16")
    train_and_evaluate(VGG19, "VGG19")

