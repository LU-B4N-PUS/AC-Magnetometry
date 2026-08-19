import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from noisy_signal import coherence_decay, lorentz_psd
from pulse_sequences import modulation, SEQUENCES

NOISE_AMPLITUDE = 1.
TAU_C = .3


def overlap_amp(T, n_pulses, omega_signal, n_points=4000):
    # integral y(t) cos(omega_signal t) dt

    t = np.linspace(0, T, n_points)
    y = modulation(t, T, n_pulses)
    return np.abs(np.trapezoid(y*np.cos(omega_signal * t), t))


def sensitivity(T, n_pulses, omega_signal):
    ov = overlap_amp(T, n_pulses, omega_signal)
    C = coherence_decay(T, n_pulses, NOISE_AMPLITUDE, TAU_C)
    denom = ov * C * np.sqrt(T)
    if denom <= 1e-12:
        return np.inf
    return 1.0 / denom


def seq_per_freq(freqs, T=1.0):
    # For each signal frequency, find the lowest sensitivity

    rows = []
    for f in freqs:
        omega_signal = 2 * np.pi * f
        row = {"freq_over_1_T": f}
        best_name, best_val = None, np.inf
        for name, n in SEQUENCES.items():
            eta = sensitivity(T, n, omega_signal)
            row[name] = eta
            if eta < best_val:
                best_val, best_name = eta, name
        row["best_seq"] = best_name
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    T = 1.0
    freqs = np.linspace(0.05, 5.0, 60)

    df = seq_per_freq(freqs, T=T)
    df.to_csv("/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/data/sensitivity_results.csv", index=False)
    print(df[["freq_over_1_T", "best_seq"]].to_string(index=False))

    fig, ax = plt.subplots(figsize=(12, 8))
    for name in SEQUENCES:
        ax.plot(df["freq_over_1_T"], df[name], label=name)
    ax.set_yscale("log")
    ax.set_xlabel("Signal frequency $f_s$ [1/T]", fontsize=18)
    ax.set_ylabel("Sensitivity metric $\eta$($f_s$)",
                  fontsize=18)  # lower = more sensitivity
    ax.set_title(
        "Which pulse sequence best detects a signal at each frequency?", fontsize=25)
    ax.legend(fontsize=10)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(
        "/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/results/sensitivity_comparison.png", dpi=300)
    print("Sensivity comparison saved in reuslts dir.")

    # SUMMARY
    win_counts = df["best_seq"].value_counts(normalize=True) * 100
    print("\nShare of frequency range where each sequence is optimal: ",
          win_counts.round(1).to_string())
