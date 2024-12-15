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
