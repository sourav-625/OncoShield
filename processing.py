# step2_feature_extraction.py

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft

# ---------------------------------
# Load raw dataset
# ---------------------------------

df = pd.read_csv("raw_multimodal_dataset.csv")

subjects = df["subject_id"].unique()
train_subjects = subjects[:int(0.8*len(subjects))]
test_subjects = subjects[int(0.8*len(subjects)):]

# ---------------------------------
# Feature extraction functions
# ---------------------------------

def spectral_entropy(x):
    psd = np.abs(fft(x))**2
    psd = psd / np.sum(psd)
    return -np.sum(psd * np.log(psd + 1e-12))

def dominant_frequency(x):
    spectrum = np.abs(fft(x))
    return np.argmax(spectrum)

def slope(x):
    return np.polyfit(range(len(x)), x, 1)[0]

# ---------------------------------
# Main feature extraction
# ---------------------------------

feature_rows = []

for idx, row in df.iterrows():

    features = {
        "subject_id": row["subject_id"],
        "time_step": row["time_step"],
        "tumor_presence": row["tumor_presence"],
        "tumor_stage": row["tumor_stage"],
        "growth_rate": row["growth_rate"]
    }


    # ---------------- PAS ----------------
    pas = row.filter(like="pas_").values
    features.update({
        "pas_energy": np.sum(pas**2),
        "pas_mean": np.mean(pas),
        "pas_std": np.std(pas),
        "pas_max": np.max(pas),
        "pas_ptp": np.ptp(pas),
        "pas_dom_freq": dominant_frequency(pas),
        "pas_entropy": spectral_entropy(pas),
        "pas_wavelet_scale1": np.sum(pas[:50]**2),
        "pas_wavelet_scale2": np.sum(pas[50:150]**2),
        "pas_wavelet_scale3": np.sum(pas[150:300]**2)
    })

    # ---------------- EIS ----------------
    eis_real = row.filter(like="eis_real_").values
    eis_imag = row.filter(like="eis_imag_").values
    magnitude = np.sqrt(eis_real**2 + eis_imag**2)
    phase = np.arctan2(eis_imag, eis_real)

    features.update({
        "eis_real_mean": np.mean(eis_real),
        "eis_imag_mean": np.mean(eis_imag),
        "eis_real_std": np.std(eis_real),
        "eis_imag_std": np.std(eis_imag),
        "eis_phase_mean": np.mean(phase),
        "eis_mag_slope": slope(np.log(magnitude + 1e-8)),
        "eis_nyquist_area": np.trapz(eis_imag, eis_real),
        "eis_mag_mean": np.mean(magnitude)
    })

    # ---------------- NIR ----------------
    nir = row.filter(like="nir_").values
    d1 = np.gradient(nir)
    d2 = np.gradient(d1)

    features.update({
        "nir_mean": np.mean(nir),
        "nir_std": np.std(nir),
        "nir_max": np.max(nir),
        "nir_min": np.min(nir),
        "nir_peak_idx": np.argmax(nir),
        "nir_d1_mean": np.mean(d1),
        "nir_d2_mean": np.mean(d2),
        "nir_auc": np.trapz(nir)
    })

    # ---------------- Thermography ----------------
    thermo = row.filter(like="thermo_").values

    features.update({
        "thermo_mean": np.mean(thermo),
        "thermo_std": np.std(thermo),
        "thermo_max": np.max(thermo),
        "thermo_final": thermo[-1],
        "thermo_rise_rate": slope(thermo),
        "thermo_energy": np.sum(thermo**2),
        "thermo_early_late": np.mean(thermo[:20]) - np.mean(thermo[-20:]),
        "thermo_ptp": np.ptp(thermo)
    })

    feature_rows.append(features)

features_df = pd.DataFrame(feature_rows)

# ---------------------------------
# Split dataset
# ---------------------------------

train_df = features_df[features_df["subject_id"].isin(train_subjects)]
test_df = features_df[features_df["subject_id"].isin(test_subjects)]

# Save files
features_df.to_csv("processed_features.csv", index=False)
train_df.to_csv("train_features.csv", index=False)
test_df.to_csv("test_features.csv", index=False)

print("Feature extraction complete.")
print("Train and test datasets saved.")
