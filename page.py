import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="OncoShield – Tumor Risk Analysis",
    layout="wide"
)

st.title("🛡️ OncoShield: Tumor Detection & Risk Assessment")
st.markdown("Multimodal Biosignal Analysis using EIS, NIRS & Thermography")

st.divider()

# -------------------------
# Sidebar Inputs (Dummy)
# -------------------------
st.sidebar.header("🧑 Patient Information")

patient_id = st.sidebar.text_input("Patient ID", "OS-1029")
age = st.sidebar.slider("Age", 18, 90, 45)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
scan_date = st.sidebar.date_input("Scan Date")

st.sidebar.divider()
st.sidebar.header("⚙️ Model Info")
st.sidebar.write("Ensemble Model:")
st.sidebar.write("- LSTM (Temporal signals)")
st.sidebar.write("- RNN (Sequential patterns)")

# -------------------------
# Dummy Model Outputs
# -------------------------
tumor_detected = True
risk_score = 0.72  # 0–1 scale
growth_rate = 1.8  # mm/month (dummy)

# -------------------------
# Detection Result Section
# -------------------------
st.subheader("🔍 Detection Result")

col1, col2, col3 = st.columns(3)

with col1:
    if tumor_detected:
        st.success("✅ Tumor Detected")
    else:
        st.success("❌ No Tumor Detected")

with col2:
    st.metric("Risk Score", f"{risk_score*100:.1f} %")

with col3:
    st.metric("Estimated Growth Rate", f"{growth_rate} mm/month")

st.divider()

# -------------------------
# Tumor Growth Trend (Dummy)
# -------------------------
st.subheader("📈 Tumor Growth Trend (Simulated)")

time = np.arange(1, 7)
tumor_size = np.array([8, 8.6, 9.4, 10.2, 11.1, 12.0])  # mm

fig1, ax1 = plt.subplots()
ax1.plot(time, tumor_size, marker='o')
ax1.set_xlabel("Time (Months)")
ax1.set_ylabel("Tumor Size (mm)")
ax1.set_title("Estimated Tumor Growth Over Time")
st.pyplot(fig1)

# -------------------------
# Signal Contribution Pie Chart
# -------------------------
st.subheader("🧬 Signal Contribution Analysis")

labels = ["EIS", "NIRS", "Thermography"]
values = [40, 35, 25]  # dummy contribution %

fig2, ax2 = plt.subplots()
ax2.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
ax2.set_title("Contribution of Biosignals")
st.pyplot(fig2)

# -------------------------
# Risk Interpretation
# -------------------------
st.subheader("⚠️ Risk Interpretation")

if risk_score < 0.3:
    st.info("Low risk – routine monitoring advised.")
elif 0.3 <= risk_score < 0.6:
    st.warning("Moderate risk – follow-up recommended.")
else:
    st.error("High risk – immediate clinical evaluation advised.")

# -------------------------
# Disclaimer
# -------------------------
st.divider()
st.caption(
    "⚠️ This system performs abnormality detection and risk assessment only. "
    "It is not a diagnostic tool."
)
