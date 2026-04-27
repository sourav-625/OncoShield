# step1_generate_raw_dataset_v2.py

import numpy as np
import pandas as pd
from scipy import signal

np.random.seed(42)

num_samples = 100
sequence_length = 10

pas_points = 500
eis_freq_points = 40
nir_points = 200
thermo_points = 100


def detrend_signal(x):
    return signal.detrend(x)


def normalize_signal(x):
    return (x - np.mean(x)) / (np.std(x) + 1e-8)


def background_subtract(x):
    return x - np.min(x)


def simulate_pas(stage, subject_variation, time_step, phenotype):

    t = np.linspace(0, 5e-6, pas_points)

    freq = (5e6 + stage*0.25e6) * subject_variation["freq_scale"]

    amplitude = (1 + stage*0.18*phenotype["pas_weight"]) * subject_variation["amp_scale"]

    p = amplitude * np.exp(-((t - 2.5e-6)**2)/(2*(0.4e-6)**2)) * np.sin(2*np.pi*freq*t)

    noise_level = np.random.uniform(0.05, 0.11)
    p += noise_level * np.random.randn(len(t))

    drift = subject_variation["drift"] * time_step
    p += drift

    instrument_bias = np.random.normal(0, 0.03)
    p += instrument_bias

    return normalize_signal(detrend_signal(p))


def simulate_eis(stage, subject_variation, phenotype):

    freq = np.logspace(2, 6, eis_freq_points)
    omega = 2*np.pi*freq

    R0 = (1000 - stage*55*phenotype["eis_weight"]) * subject_variation["imp_scale"]
    Rinf = (200 - stage*10*phenotype["eis_weight"]) * subject_variation["imp_scale"]

    tau = 1e-4 + stage*2e-5
    alpha = 0.9 - stage*0.025

    Z = Rinf + (R0 - Rinf)/(1 + (1j*omega*tau)**alpha)

    noise = np.random.uniform(0.025, 0.055)

    real_part = np.real(Z) + noise*np.random.randn(len(freq))
    imag_part = np.imag(Z) + noise*np.random.randn(len(freq))

    electrode_shift = np.random.normal(0, 4)

    real_part += electrode_shift
    imag_part += electrode_shift*0.5

    return normalize_signal(real_part), normalize_signal(imag_part)


def simulate_nir(stage, subject_variation, phenotype):

    wavelength = np.linspace(700, 900, nir_points)

    peak_shift = 800 + stage*2.5*phenotype["nir_weight"] + subject_variation["nir_shift"]

    absorbance = np.exp(-0.01*(wavelength - peak_shift)**2)

    noise = np.random.uniform(0.02, 0.055)
    absorbance += noise*np.random.randn(len(wavelength))

    scattering = np.random.normal(1.0, 0.07)
    absorbance *= scattering

    return normalize_signal(background_subtract(absorbance))


def simulate_thermo(stage, subject_variation, time_step, phenotype):

    t = np.linspace(0, 60, thermo_points)

    baseline_temp = subject_variation["baseline_temp"]

    delta_T = (1 + stage*0.28*phenotype["thermo_weight"]) * subject_variation["thermal_scale"]

    tau = 20 + stage*2.5

    T = baseline_temp + delta_T*(1 - np.exp(-t/tau))

    noise = np.random.uniform(0.05, 0.09)
    T += noise*np.random.randn(len(t))

    drift = subject_variation["drift"] * time_step
    T += drift

    camera_bias = np.random.normal(0, 0.06)
    T += camera_bias

    return normalize_signal(T)


rows = []

for subject in range(num_samples):

    subject_variation = {
        "baseline_temp": 36.5 + np.random.normal(0, 0.5),
        "imp_scale": np.random.normal(1.0, 0.1),
        "thermal_scale": np.random.normal(1.0, 0.18),
        "freq_scale": np.random.normal(1.0, 0.1),
        "amp_scale": np.random.normal(1.0, 0.1),
        "nir_shift": np.random.normal(0, 4),
        "drift": np.random.normal(0, 0.02)
    }

    # tumor phenotype variability (different biological behaviour)
    phenotype = {
        "pas_weight": np.random.uniform(0.6, 1.4),
        "eis_weight": np.random.uniform(0.6, 1.4),
        "nir_weight": np.random.uniform(0.6, 1.4),
        "thermo_weight": np.random.uniform(0.6, 1.4)
    }

    tumor_presence = np.random.randint(0, 2)

    benign_anomaly = np.random.rand() < 0.30

    if tumor_presence == 1:
        initial_stage = np.random.randint(1, 3)
        growth_rate = np.random.uniform(0.1, 0.4)
    else:
        initial_stage = 0
        growth_rate = 0

    midpoint = np.random.uniform(3, 7)

    for time_step in range(sequence_length):

        if tumor_presence == 1:
            logistic = 3 / (1 + np.exp(-growth_rate*(time_step - midpoint)))
            stage = int(min(initial_stage + logistic, 3))
        else:
            stage = 0

        if benign_anomaly and tumor_presence == 0:
            stage_effect = np.random.uniform(0.15, 0.55)
        else:
            stage_effect = 0

        effective_stage = stage + stage_effect

        pas = simulate_pas(effective_stage, subject_variation, time_step, phenotype)
        eis_r, eis_i = simulate_eis(effective_stage, subject_variation, phenotype)
        nir = simulate_nir(effective_stage, subject_variation, phenotype)
        thermo = simulate_thermo(effective_stage, subject_variation, time_step, phenotype)

        row = {
            "subject_id": subject,
            "time_step": time_step,
            "tumor_presence": tumor_presence,
            "tumor_stage": stage,
            "growth_rate": growth_rate
        }

        for i, val in enumerate(pas):
            row[f"pas_{i}"] = val

        for i, val in enumerate(eis_r):
            row[f"eis_real_{i}"] = val

        for i, val in enumerate(eis_i):
            row[f"eis_imag_{i}"] = val

        for i, val in enumerate(nir):
            row[f"nir_{i}"] = val

        for i, val in enumerate(thermo):
            row[f"thermo_{i}"] = val

        rows.append(row)

df = pd.DataFrame(rows)

df.to_csv("raw_multimodal_dataset.csv", index=False)

print("Extended dataset saved.")