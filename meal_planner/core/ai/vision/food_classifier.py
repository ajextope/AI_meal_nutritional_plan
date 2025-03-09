import tensorflow as tf
from tensorflow.keras import layers

class FoodVisionClassifier:
    def __init__(self, input_shape=(224, 224, 3), num_classes=10):
        self.model = self.build_model(input_shape, num_classes)
        
    def build_model(self, input_shape, num_classes):
        model = tf.keras.Sequential([
            layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64, (3,3), activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(128, (3,3), activation='relu'),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])
        model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])
        return model
    
    def predict_food(self, image_path):
        # Implement actual prediction logic
        return {"food_item": "Salad", "confidence": 0.92}