# step4b_train_lstm_growth.py

import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from tensorflow.keras import layers, models

# ---------------------------------
# Load processed features
# ---------------------------------

train_df = pd.read_csv("train_features.csv")

selected_features = joblib.load("svm_selected_features.pkl")

subjects = train_df["subject_id"].unique()

X = []
y = []

for subject in subjects:
    subject_data = train_df[train_df["subject_id"] == subject]
    subject_data = subject_data.sort_values("time_step")

    feature_seq = subject_data[selected_features].values
    growth_rate = subject_data["growth_rate"].iloc[0]

    X.append(feature_seq)
    y.append(growth_rate)

X = np.array(X)
y = np.array(y)

# ---------------------------------
# Build LSTM Regression Model
# ---------------------------------

model = models.Sequential([
    layers.LSTM(64, return_sequences=True,
                input_shape=(X.shape[1], X.shape[2])),
    layers.Dropout(0.3),

    layers.LSTM(32),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="linear")  # regression
])

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)

# ---------------------------------
# Train
# ---------------------------------

model.fit(
    X, y,
    epochs=25,
    batch_size=8,
    validation_split=0.2
)

model.save("lstm_growth_model.h5")

print("LSTM growth model saved.")
