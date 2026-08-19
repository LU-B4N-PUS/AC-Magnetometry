import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from env_dataset import lab_dataset
from pulse_sequences import modulation, SEQUENCES
from analysis import overlap_amp
from noisy_signal import GAMMA


#   "/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/data/

TARGET = 50.0
T_SHOT = 1.14794 / TARGET
READOUT_REPS = 50


def run_experiment(n_pulses, df, sample_rate, seed):
    rng = np.random.default_rng(seed)
    sample_per_shot = int(T_SHOT * sample_rate)
    n_shots = len(df) // sample_per_shot

    shot_times = np.zeros(n_shots)
    phi_hat = np.zeros(n_shots)

    for k in range(n_shots):
        sl = slice(k * sample_per_shot, (k+1)*sample_per_shot)
        t_window = df['time_s'].values[sl]
        B_window = df['B_total'].values[sl]
        t_local = t_window - t_window[0]
        shot_times[k] = t_window[0]

        y = modulation(t_local, T_SHOT, n_pulses)
        phi = GAMMA * np.trapezoid(y * B_window, t_local)
        p = 0.5 * (1 + np.sin(phi))
        p = np.clip(p, 0, 1)
        clicks = rng.binomial(READOUT_REPS, p) / READOUT_REPS
        phi_hat[k] = np.arcsin(np.clip(2*clicks-1, -1, 1))

    # Software lock-in
    omega_t = 2 * np.pi * TARGET * shot_times
    design = np.column_stack([np.cos(omega_t), np.sin(omega_t)])
    coeffs, *_ = np.linalg.lstsq(design, phi_hat, rcond=None)
    a, b = coeffs
    raw_amp = np.hypot(a, b)

    omega_signal = 2*np.pi*TARGET
    gain = GAMMA * overlap_amp(T_SHOT, n_pulses, omega_signal)
    B_estimated = raw_amp / gain if gain > 1e-9 else np.nan

    return B_estimated, shot_times, phi_hat


def monte_carlo_comparison(n_trial=20, B_signal=1.0):
    row = []
    for trial in range(n_trial):
        df = lab_dataset(duration=5., b_signal=B_signal, seed=1000 + trial)
        sample_rate = 1 / (df['time_s'][1] - df['time_s'][0])
        for name, n in SEQUENCES.items():
            B_est, _, _ = run_experiment(n, df, sample_rate, seed=2000 + trial)
            row.append({
                "trial": trial,
                "sequence": name,
                "B_true": B_signal,
                "B_estimated": B_est,
                "abs_error": abs(B_est - B_signal),
            })

    return pd.DataFrame(row)


if __name__ == "__main__":
    results = monte_carlo_comparison(n_trial=20)
    # results.to_csv("/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/data/sensing_results.csv", index=False)

    summary = results.groupby("sequence").agg(
        mean_estimate=("B_estimated", "mean"),
        std_estimate=("B_estimated", "std"),
        mean_abs_error=("abs_error", "mean"),
    ).reindex(SEQUENCES.keys())

    print(summary.round(4))
    # summary.to_csv("/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/data/sensing_summary.csv")

    fig, ax = plt.subplots(figsize=(12, 8))
    order = list(SEQUENCES.keys())
    data = [results[results["sequence"] == s]
            ["B_estimated"].values for s in order]
    bp = ax.boxplot(data, tick_labels=order, patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("cornflowerblue")
    ax.axhline(1.5, color='orange', ls="--", label="true B_signal = 1.0")
    ax.set_ylabel("Estimated cable amplitude", fontsize=18)
    ax.set_title(
        f"Recovering a 50 Hz signal from the lab dataset\n(20 independent noise realizations per sequence)", fontsize=25)
    ax.legend(fontsize=15)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(
        "/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/results/sensing_experiment_results.png", dpi=300)
    print("\nSaved sensing_experiment_results.png in results dir, and sensing_results.csv, sensing_summary.csv in data dir")
