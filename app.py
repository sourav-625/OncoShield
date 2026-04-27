# step5_clinical_driver.py

import numpy as np
import pandas as pd
import joblib
import tensorflow as tf

# ---------------------------------
# Load everything
# ---------------------------------

test_features = pd.read_csv("test_features.csv")
raw_data = pd.read_csv("raw_multimodal_dataset.csv")

svm = joblib.load("svm_model.pkl")
scaler = joblib.load("svm_scaler.pkl")
selected_features = joblib.load("svm_selected_features.pkl")

cnn_model = tf.keras.models.load_model("cnn_stage_model.h5", compile=False)
lstm_model = tf.keras.models.load_model("lstm_growth_model.h5", compile=False)


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("\n========== MODEL PERFORMANCE SUMMARY ==========\n")

# ---------------------------------
# SVM Evaluation
# ---------------------------------

X_test = test_features[selected_features].values
y_test = test_features["tumor_presence"].values

X_test_scaled = scaler.transform(X_test)
svm_test_preds = svm.predict(X_test_scaled)

svm_accuracy = accuracy_score(y_test, svm_test_preds)
svm_precision = precision_score(y_test, svm_test_preds)
svm_recall = recall_score(y_test, svm_test_preds)
svm_f1 = f1_score(y_test, svm_test_preds)

print("SVM Tumor Detection Performance:")
print(f" - Accuracy:  {svm_accuracy:.3f}")
print(f" - Precision: {svm_precision:.3f}")
print(f" - Recall:    {svm_recall:.3f}")
print(f" - F1 Score:  {svm_f1:.3f}")
print(" - Confusion Matrix:")
print(confusion_matrix(y_test, svm_test_preds))
print()

# ---------------------------------
# CNN Stage Evaluation
# ---------------------------------

X_cnn_test = []
y_stage_test = []

for subject in test_features["subject_id"].unique():
    raw_subject = raw_data[raw_data["subject_id"] == subject]
    raw_subject = raw_subject.sort_values("time_step")

    pas_signals = []
    for _, row in raw_subject.iterrows():
        pas = row.filter(like="pas_").values
        pas_signals.append(pas)

    if len(pas_signals) > 0:
        X_cnn_test.extend(pas_signals)
        stage_vals = raw_subject["tumor_stage"].values
        y_stage_test.extend(stage_vals)

X_cnn_test = np.array(X_cnn_test)[..., np.newaxis]
y_stage_test = np.array(y_stage_test)

cnn_preds = cnn_model.predict(X_cnn_test, verbose=0)
cnn_classes = np.argmax(cnn_preds, axis=1)

cnn_accuracy = accuracy_score(y_stage_test, cnn_classes)

print("CNN Stage Classification Performance:")
print(f" - Accuracy: {cnn_accuracy:.3f}")
print(" - Confusion Matrix:")
print(confusion_matrix(y_stage_test, cnn_classes))
print()

# ---------------------------------
# LSTM Growth Rate Evaluation
# ---------------------------------

y_growth_test = test_features.groupby("subject_id")["growth_rate"].first().values

X_lstm_test = []
for subject in test_features["subject_id"].unique():
    subject_data = test_features[test_features["subject_id"] == subject]
    subject_data = subject_data.sort_values("time_step")
    X_seq = subject_data[selected_features].values
    X_lstm_test.append(X_seq)

X_lstm_test = np.array(X_lstm_test)

lstm_preds = lstm_model.predict(X_lstm_test, verbose=0).flatten()

mae = mean_absolute_error(y_growth_test, lstm_preds)
mse = mean_squared_error(y_growth_test, lstm_preds)
r2 = r2_score(y_growth_test, lstm_preds)

print("LSTM Growth Rate Prediction Performance:")
print(f" - MAE: {mae:.4f}")
print(f" - MSE: {mse:.4f}")
print(f" - R² Score: {r2:.4f}")
print("\n==============================================\n")

# ---------------------------------
# Get test subjects
# ---------------------------------

test_subjects = test_features["subject_id"].unique()

print("\n========== MULTIMODAL DIAGNOSTIC REPORT ==========\n")

for subject in test_subjects:

    print(f"Patient ID: {subject}")
    print("----------------------------------------------")

    # ---------------------------------
    # SVM Screening
    # ---------------------------------

    subject_data = test_features[test_features["subject_id"] == subject]
    subject_data = subject_data.sort_values("time_step")

    X_svm = subject_data[selected_features].values
    X_svm_scaled = scaler.transform(X_svm)

    svm_preds = svm.predict(X_svm_scaled)
    svm_final = int(np.round(np.mean(svm_preds)))

    if svm_final == 0:
        print("Screening Result: NO TUMOR DETECTED")
        print("Recommendation: Routine monitoring.\n")
        continue

    print("Screening Result: TUMOR DETECTED")
    print("Proceeding to structural & temporal analysis...\n")

    # ---------------------------------
    # CNN Stage Prediction
    # ---------------------------------

    raw_subject = raw_data[raw_data["subject_id"] == subject]
    raw_subject = raw_subject.sort_values("time_step")

    X_cnn = []

    for _, row in raw_subject.iterrows():
        pas = row.filter(like="pas_").values
        X_cnn.append(pas)

    X_cnn = np.array(X_cnn)[..., np.newaxis]

    stage_probs = cnn_model.predict(X_cnn, verbose=0)
    stage_preds = np.argmax(stage_probs, axis=1)

    final_stage = int(np.round(np.mean(stage_preds)))

    stage_map = {
        0: "No Structural Tumor Pattern",
        1: "Early Stage",
        2: "Intermediate Stage",
        3: "Advanced Stage"
    }

    print(f"Predicted Tumor Stage: {stage_map[final_stage]}")

    # ---------------------------------
    # LSTM Growth Rate Prediction
    # ---------------------------------

    X_lstm = subject_data[selected_features].values
    X_lstm = np.expand_dims(X_lstm, axis=0)

    predicted_growth = float(lstm_model.predict(X_lstm, verbose=0)[0][0])

    print(f"Estimated Growth Rate: {predicted_growth:.3f}")

    # ---------------------------------
    # Risk Interpretation Layer
    # ---------------------------------

    if predicted_growth < 0.15:
        aggressiveness = "Slow Growing"
    elif predicted_growth < 0.30:
        aggressiveness = "Moderately Aggressive"
    else:
        aggressiveness = "Highly Aggressive"

    print(f"Aggressiveness Category: {aggressiveness}")

    # Clinical summary
    print("\nClinical Interpretation:")

    if final_stage == 1 and predicted_growth < 0.2:
        print(" - Early localized tumor.")
        print(" - Good prognosis with early intervention.")
    elif final_stage == 2:
        print(" - Tumor progression evident.")
        print(" - Requires immediate specialist evaluation.")
    elif final_stage == 3:
        print(" - Advanced tumor characteristics detected.")
        print(" - High priority medical intervention advised.")
    else:
        print(" - Inconsistent structural pattern. Further imaging recommended.")

    print("\n----------------------------------------------\n")

print("========== REPORT COMPLETE ==========")
