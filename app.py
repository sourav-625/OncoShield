import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Import ONLY inference-related functions
from Model import predict_oncoshield, load_oncoshield_model

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="OncoShield – Risk Analysis",
    layout="wide"
)

st.title("🛡️ OncoShield: Multimodal Abnormality Detection")
st.caption("Thermography + Bio-Impedance | Ensemble CNN–LSTM Model")

st.divider()

# -------------------------
# Load Model Once
# -------------------------
@st.cache_resource
def load_model():
    return load_oncoshield_model()

model = load_model()

# -------------------------
# Sidebar – Input Controls
# -------------------------
st.sidebar.header("🔬 Scan Controls")

use_dummy = st.sidebar.checkbox("Use Dummy Input", value=True)

if use_dummy:
    thermal_image = np.random.rand(64, 64, 3).astype(np.float32)
    bio_series = np.random.rand(50, 10).astype(np.float32)
else:
    st.sidebar.warning("Real input upload not implemented yet.")
    thermal_image = np.random.rand(64, 64, 3).astype(np.float32)
    bio_series = np.random.rand(50, 10).astype(np.float32)

# -------------------------
# Run Inference
# -------------------------
if st.button("🚀 Run OncoShield Analysis"):

    result = predict_oncoshield(
        thermal_image=thermal_image,
        bioimpedance_series=bio_series
    )

    # -------------------------
    # Result Overview
    # -------------------------
    st.subheader("🔍 Detection Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        if result["class_index"] == 1:
            st.error(result["prediction"])
        else:
            st.success(result["prediction"])

    with col2:
        st.metric(
            "Model Confidence",
            f"{result['confidence'] * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Predicted Class Index",
            result["class_index"]
        )

    st.divider()

    # -------------------------
    # Raw Softmax Scores
    # -------------------------
    st.subheader("🧠 Model Output Scores")
    st.json(result["raw_scores"])

    # -------------------------
    # Dummy Tumor Growth Curve
    # -------------------------
    st.subheader("📈 Estimated Growth Trend (Simulated)")

    months = np.arange(1, 7)
    growth = np.cumsum(np.random.uniform(0.5, 1.2, size=6)) + 6

    fig1, ax1 = plt.subplots()
    ax1.plot(months, growth, marker="o")
    ax1.set_xlabel("Time (Months)")
    ax1.set_ylabel("Estimated Size (mm)")
    ax1.set_title("Tumor Growth Projection")
    st.pyplot(fig1)

    # -------------------------
    # Dummy Modality Contribution
    # -------------------------
    st.subheader("🧬 Modality Contribution (Simulated)")

    labels = ["Thermal/NIR CNN", "Bio-Impedance LSTM"]
    values = [55, 45]

    fig2, ax2 = plt.subplots()
    ax2.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax2.set_title("Ensemble Contribution")
    st.pyplot(fig2)

    # -------------------------
    # Interpretation Layer
    # -------------------------
    st.subheader("⚠️ Risk Interpretation")

    if result["confidence"] < 0.4:
        st.info("Low risk signal – routine monitoring suggested.")
    elif result["confidence"] < 0.7:
        st.warning("Moderate risk signal – follow-up recommended.")
    else:
        st.error("High risk signal – clinical evaluation advised.")

    st.caption(
        "⚠️ This system performs abnormality detection and risk estimation only. "
        "It is not a diagnostic tool."
    )
