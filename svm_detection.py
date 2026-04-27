# step3_train_svm_mrmr.py

import numpy as np
import pandas as pd
import joblib

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score


# ==========================================================
# 1. Load Data
# ==========================================================

train_df = pd.read_csv("train_features.csv")

X = train_df.drop(columns=[
    "subject_id",
    "time_step",
    "tumor_presence",
    "tumor_stage",
    "growth_rate"
])

y = train_df["tumor_presence"].values

feature_names = X.columns.tolist()
X_values = X.values

print("Total features before selection:", len(feature_names))


# ==========================================================
# 2. mRMR Feature Selection
# ==========================================================

def mrmr_selection(X, y, feature_names, k=15):
    """
    Minimal Redundancy Maximal Relevance
    """

    n_features = X.shape[1]

    relevance = mutual_info_classif(X, y)

    selected = []
    remaining = list(range(n_features))

    # First feature (max relevance)
    first = np.argmax(relevance)
    selected.append(first)
    remaining.remove(first)

    corr_matrix = np.corrcoef(X, rowvar=False)

    while len(selected) < k:

        best_score = -np.inf
        best_feature = None

        for idx in remaining:

            rel = relevance[idx]

            redundancy = np.mean([
                abs(corr_matrix[idx, s]) for s in selected
            ])

            score = rel - redundancy

            if score > best_score:
                best_score = score
                best_feature = idx

        selected.append(best_feature)
        remaining.remove(best_feature)

    return [feature_names[i] for i in selected]


# ==========================================================
# 3. Time-Series Cross Validation
# ==========================================================

tscv = TimeSeriesSplit(n_splits=5)

cv_scores = []

for fold, (train_idx, val_idx) in enumerate(tscv.split(X_values)):

    X_train, X_val = X_values[train_idx], X_values[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    # Feature selection INSIDE CV
    selected_features = mrmr_selection(
        X_train,
        y_train,
        feature_names,
        k=15
    )

    selected_indices = [feature_names.index(f) for f in selected_features]

    X_train_sel = X_train[:, selected_indices]
    X_val_sel = X_val[:, selected_indices]

    # Scaling (fit ONLY on training)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_sel)
    X_val_scaled = scaler.transform(X_val_sel)

    svm = SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        probability=True
    )

    svm.fit(X_train_scaled, y_train)

    preds = svm.predict(X_val_scaled)

    acc = accuracy_score(y_val, preds)

    cv_scores.append(acc)

    print(f"Fold {fold+1} Accuracy: {acc:.4f}")

print("\nMean CV Accuracy:", np.mean(cv_scores))


# ==========================================================
# 4. Final Feature Selection (Full Data)
# ==========================================================

selected_features = mrmr_selection(
    X_values,
    y,
    feature_names,
    k=15
)

print("\nFinal Selected Features:")
for f in selected_features:
    print(" -", f)

selected_indices = [feature_names.index(f) for f in selected_features]

X_selected = X_values[:, selected_indices]


# ==========================================================
# 5. Final Model Training
# ==========================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_selected)

svm = SVC(
    kernel="rbf",
    C=1.0,
    gamma="scale",
    probability=True
)

svm.fit(X_scaled, y)


# ==========================================================
# 6. Save Model
# ==========================================================

joblib.dump(svm, "svm_model.pkl")
joblib.dump(selected_features, "svm_selected_features.pkl")
joblib.dump(scaler, "svm_scaler.pkl")

print("\nSVM model, selected features, and scaler saved successfully.")