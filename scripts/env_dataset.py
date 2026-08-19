import numpy as np
import pandas as pd

RANDOM_SEED = 42


def lab_dataset(duration=5.0, sample_rate=4000., b_signal=1., seed=RANDOM_SEED):
    rng = np.random.default_rng(seed)
    n_samples = int(duration * sample_rate)
    t = np.arange(n_samples) / sample_rate

    cable = (b_signal * np.cos(2*np.pi * 50 * t) +
             0.35 * b_signal * np.cos(2*np.pi * 100 * t + 0.4)
             + 0.15 * b_signal * np.cos(2*np.pi * 150 * t + 1.1))

    motor = 0.8 * b_signal * np.cos(2*np.pi*23*t + rng.uniform(0, 2*np.pi))
    other_device = 0.6*b_signal * \
        np.cos(2*np.pi*62*t + rng.uniform(0, 2 * np.pi))

    TAU_C = 0.4
    dt = 1 / sample_rate
    alpha = np.exp(-dt/TAU_C)
    drift_amp = 1.2*b_signal
    drift = np.zeros(n_samples)
    psd_drift = rng.normal(0, drift_amp * np.sqrt(1-alpha**2), n_samples)
    for i in range(1, n_samples):
        drift[i] = alpha * drift[i-1] + psd_drift[i]

    white_noise = rng.normal(0, 0.25*b_signal, n_samples)
    b_total = cable + motor + other_device + drift + white_noise

    df = pd.DataFrame({
        "time_s": t,
        "B_total": b_total,
        "B_cabel_only": cable,
        "B_motor": motor,
        "B_other_device": other_device,
        "B_drift": drift,
        "B_white_noise": white_noise,
    }
    )

    return df


if __name__ == "__main__":
    df = lab_dataset()
    df.to_csv("/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/data/lab_dataset.csv", index=False)
    print(f"saved lab_dataset.csv in data dir: {len(df)} samples,",
          f"{df['time_s'].iloc[-1]:.2f} s at {1/(df['time_s'][1]- df['time_s'][0]):.0f} Hz")
    print(df.head())
