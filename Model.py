import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense,
    LSTM, Dropout, Input, concatenate
)
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import cv2
import os

# =========================
# PARAMETERS
# =========================
NUM_SAMPLES = 1000
IMAGE_SIZE = (64, 64, 3)
TIME_STEPS = 50
FEATURES_BIO = 10
NUM_CLASSES = 2
EPOCHS = 10
BATCH_SIZE = 32
MODEL_DIR = "saved_models"
MODEL_NAME = "oncoshield_ensemble.keras"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

os.makedirs(MODEL_DIR, exist_ok=True)

_loaded_model = None  # cache for inference

# =========================
# DATA GENERATION
# =========================
def generate_structured_images(num_samples, image_size):
    images, labels = [], []

    for _ in range(num_samples):
        img = np.zeros(image_size, dtype=np.uint8)

        if np.random.rand() > 0.5:
            center = (np.random.randint(20, 44), np.random.randint(20, 44))
            cv2.circle(img, center, 10, (255, 0, 0), -1)
            label = 1
        else:
            label = 0

        images.append(img / 255.0)
        labels.append(label)

    return np.array(images), np.array(labels)


def generate_structured_bioimpedance(num_samples, time_steps, features_bio):
    data, labels = [], []

    for _ in range(num_samples):
        if np.random.rand() > 0.5:
            base = np.sin(np.linspace(0, 2*np.pi, time_steps)).reshape(-1, 1)
            noise = np.random.rand(time_steps, features_bio) * 0.5
            series = base + noise
            label = 1
        else:
            base = 0.2 * np.sin(np.linspace(0, 2*np.pi, time_steps)).reshape(-1, 1)
            noise = np.random.rand(time_steps, features_bio) * 0.1
            series = base + noise
            label = 0

        data.append(series)
        labels.append(label)

    return np.array(data), np.array(labels)

# =========================
# MODEL DEFINITIONS
# =========================
def create_cnn():
    inp = Input(shape=IMAGE_SIZE)
    x = Conv2D(32, 3, activation="relu", padding="same")(inp)
    x = MaxPooling2D()(x)
    x = Conv2D(64, 3, activation="relu", padding="same")(x)
    x = MaxPooling2D()(x)
    x = Conv2D(128, 3, activation="relu", padding="same")(x)
    x = MaxPooling2D()(x)
    x = Flatten()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.5)(x)
    out = Dense(64, activation="relu")(x)

    return Model(inp, out, name="Thermal_NIR_CNN")


def create_lstm():
    inp = Input(shape=(TIME_STEPS, FEATURES_BIO))
    x = LSTM(64, return_sequences=True)(inp)
    x = LSTM(64)(x)
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.5)(x)
    out = Dense(64, activation="relu")(x)

    return Model(inp, out, name="BioImpedance_LSTM")

# =========================
# ENSEMBLE MODEL
# =========================
def build_oncoshield_model():
    cnn = create_cnn()
    lstm = create_lstm()

    combined = concatenate([cnn.output, lstm.output])
    x = Dense(128, activation="relu")(combined)
    x = Dropout(0.5)(x)
    output = Dense(NUM_CLASSES, activation="softmax")(x)

    model = Model(
        inputs=[cnn.input, lstm.input],
        outputs=output,
        name="OncoShield_Ensemble"
    )

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

# =========================
# TRAINING PIPELINE
# =========================
def train_and_evaluate():
    X_img, y_img = generate_structured_images(NUM_SAMPLES, IMAGE_SIZE)
    X_bio, _ = generate_structured_bioimpedance(NUM_SAMPLES, TIME_STEPS, FEATURES_BIO)

    y = to_categorical(y_img, NUM_CLASSES)

    X_img_tr, X_img_te, X_bio_tr, X_bio_te, y_tr, y_te = train_test_split(
        X_img, X_bio, y, test_size=0.2, random_state=42
    )

    model = build_oncoshield_model()
    model.summary()

    model.fit(
        [X_img_tr, X_bio_tr],
        y_tr,
        validation_data=([X_img_te, X_bio_te], y_te),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )

    loss, acc = model.evaluate([X_img_te, X_bio_te], y_te)
    print(f"\nTest Accuracy: {acc * 100:.2f}%")

    model.save(MODEL_PATH)
    print(f"\nModel saved at: {MODEL_PATH}")

    return model

# =========================
# MODEL LOADING (INFERENCE)
# =========================
def load_oncoshield_model():
    global _loaded_model

    if _loaded_model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Saved OncoShield model not found.")
        _loaded_model = tf.keras.models.load_model(MODEL_PATH)
        print("OncoShield model loaded.")

    return _loaded_model

# =========================
# INFERENCE FUNCTION
# =========================
def predict_oncoshield(thermal_image, bioimpedance_series):
    """
    thermal_image: np.ndarray of shape (64, 64, 3)
    bioimpedance_series: np.ndarray of shape (50, 10)
    """

    model = load_oncoshield_model()

    if thermal_image.shape != IMAGE_SIZE:
        raise ValueError("Invalid thermal image shape")

    if bioimpedance_series.shape != (TIME_STEPS, FEATURES_BIO):
        raise ValueError("Invalid bio-impedance shape")

    thermal_image = np.expand_dims(thermal_image, axis=0)
    bioimpedance_series = np.expand_dims(bioimpedance_series, axis=0)

    preds = model.predict([thermal_image, bioimpedance_series], verbose=0)[0]
    cls = np.argmax(preds)

    return {
        "prediction": "Cancer Detected" if cls == 1 else "No Cancer Detected",
        "class_index": int(cls),
        "confidence": float(preds[cls]),
        "raw_scores": preds.tolist()
    }

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    train_and_evaluate()
