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

