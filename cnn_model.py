# step4a_train_cnn_stage.py

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models

# ---------------------------------
# Load dataset
# ---------------------------------

df = pd.read_csv("raw_multimodal_dataset.csv")

subjects = df["subject_id"].unique()
train_subjects = subjects[:int(0.8*len(subjects))]
test_subjects = subjects[int(0.8*len(subjects)):]

train_df = df[df["subject_id"].isin(train_subjects)]
test_df = df[df["subject_id"].isin(test_subjects)]

# ---------------------------------
# Extract PAS + Stage
# ---------------------------------

def extract_pas_stage(dataframe):
    X = []
    y = []

    for _, row in dataframe.iterrows():
        pas = row.filter(like="pas_").values
        X.append(pas)
        y.append(row["tumor_stage"])

    return np.array(X), np.array(y)

X_train, y_train = extract_pas_stage(train_df)
X_test, y_test = extract_pas_stage(test_df)

X_train = X_train[..., np.newaxis]
X_test = X_test[..., np.newaxis]

# ---------------------------------
# Build CNN
# ---------------------------------

model = models.Sequential([
    layers.Conv1D(32, 5, activation="relu",
                  input_shape=(X_train.shape[1],1)),
    layers.MaxPooling1D(2),

    layers.Conv1D(64, 5, activation="relu"),
    layers.MaxPooling1D(2),

    layers.Conv1D(128, 3, activation="relu"),
    layers.GlobalAveragePooling1D(),

    layers.Dense(64, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(4, activation="softmax")   # 4-stage output
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ---------------------------------
# Train
# ---------------------------------

model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=16,
    validation_split=0.1
)

model.save("cnn_stage_model.h5")

print("CNN stage model saved.")
