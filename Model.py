import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, LSTM, Dropout, Input, concatenate
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import cv2
import matplotlib.pyplot as plt
from . import requests

# Parameters
num_samples = 1000  # Simulated sample count
image_size = (64, 64, 3)  # Image dimensions (Thermography & NIR)
time_steps = 50  # Time steps for bio-impedance signals
features_bio = 10  # Features in bio-impedance data
num_classes = 2  # Cancer (1) or No Cancer (0)

# Generate structured image data for Thermography & NIR imaging
def generate_structured_images(num_samples, image_size):
    images = []
    labels = []
    for _ in range(num_samples):
        img = np.zeros(image_size, dtype=np.uint8)
        if np.random.rand() > 0.5:  # 50% chance of being cancerous
            # Add a hotspot to simulate abnormal thermal region
            center = (np.random.randint(20, 44), np.random.randint(20, 44))
            cv2.circle(img, center, 10, (255, 0, 0), -1)
            label = 1  # Cancerous
        else:
            label = 0  # Non-cancerous
        images.append(img / 255.0)  # Normalize
        labels.append(label)
    return np.array(images), np.array(labels)

# Generate structured bio-impedance data
def generate_structured_bioimpedance(num_samples, time_steps, features_bio):
    data = []
    labels = []
    
    for _ in range(num_samples):
        if np.random.rand() > 0.5:
            # Cancerous pattern: Higher fluctuations
            base_signal = np.sin(np.linspace(0, 6.28, time_steps)).reshape(-1, 1)
            noise = np.random.rand(time_steps, features_bio) * 0.5
            series = base_signal + noise
            label = 1
        else:
            # Normal pattern: Stable low-frequency response
            base_signal = (np.sin(np.linspace(0, 6.28, time_steps)) * 0.2).reshape(-1, 1)
            noise = np.random.rand(time_steps, features_bio) * 0.1
            series = base_signal + noise
            label = 0
        
        data.append(series)
        labels.append(label)
    
    return np.array(data), np.array(labels)

# Generate structured dataset
X_images, y_images = generate_structured_images(num_samples, image_size)
X_bio, y_bio = generate_structured_bioimpedance(num_samples, time_steps, features_bio)

# Ensure both labels are consistent
y = to_categorical(y_images, num_classes)

# Split data
X_images_train, X_images_test, X_bio_train, X_bio_test, y_train, y_test = train_test_split(
    X_images, X_bio, y, test_size=0.2, random_state=42)

# CNN Model for Thermography & NIR Images
def create_cnn():
    cnn_input = Input(shape=image_size)
    x = Conv2D(32, (3,3), activation='relu', padding='same')(cnn_input)
    x = MaxPooling2D((2,2))(x)
    x = Conv2D(64, (3,3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2,2))(x)
    x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2,2))(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    cnn_output = Dense(64, activation='relu')(x)
    return Model(inputs=cnn_input, outputs=cnn_output)

# LSTM Model for Bio-Impedance Time-Series Data
def create_lstm():
    lstm_input = Input(shape=(time_steps, features_bio))
    x = LSTM(64, return_sequences=True)(lstm_input)
    x = LSTM(64)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.5)(x)
    lstm_output = Dense(64, activation='relu')(x)
    return Model(inputs=lstm_input, outputs=lstm_output)

# Create CNN and LSTM models
cnn_model = create_cnn()
lstm_model = create_lstm()

# Combine CNN and LSTM outputs
combined_input = concatenate([cnn_model.output, lstm_model.output])
x = Dense(128, activation='relu')(combined_input)
x = Dropout(0.5)(x)
final_output = Dense(num_classes, activation='softmax')(x)

# Final Ensemble Model
ensemble_model = Model(inputs=[cnn_model.input, lstm_model.input], outputs=final_output)
ensemble_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the Model
ensemble_model.fit([X_images_train, X_bio_train], y_train, validation_data=([X_images_test, X_bio_test], y_test),
                   epochs=10, batch_size=32)

# Evaluate the Model
loss, accuracy = ensemble_model.evaluate([X_images_test, X_bio_test], y_test)
print(f'Test Accuracy: {accuracy * 100:.2f}%')
