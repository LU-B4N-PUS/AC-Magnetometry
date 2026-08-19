import numpy as np
import matplotlib.pyplot as plt


def modulation(t, T, n_pulses):
    """
     t : array_like
        Time points, 0 <= t <= T
    T : float
        Total sensing time
    n_pulses : int
        Number of pi-pulses.

    Returns
    y : array, values in {+1, -1}
    """
    t = np.asarray(t)
    if n_pulses == 0:
        return np.ones_like(t)

    spacing = T / n_pulses
    # shifting by half from the sequence edge
    pulse_time = spacing * (np.arange(n_pulses) + 0.5)

    y = np.ones_like(t)
    for i in pulse_time:
        y = np.where(t >= i, -y, y)  # filps sign each pulse
    return y


SEQUENCES = {
    "Ramsey": 0,
    "Hahn Echo": 1,
    "CPMG-2": 2,
    "CPMG-4": 4,
    "CPMG-8": 8,

}


if __name__ == "__main__":
    T = 1.0
    t = np.linspace(0, T, 1000)

    fig, axes = plt.subplots(len(SEQUENCES), 1, figsize=(8, 10), sharex=True)

    for ax, (name, n) in zip(axes, SEQUENCES.items()):
        y = modulation(t, T, n)
        ax.step(t, y, where="post")
        ax.set_ylabel(name, fontsize=12)
        # ax.set_xlabel("Time [s]", fontsize=12)
        ax.set_ylim(-1.2, 1.2)

    axes[-1].set_xlabel("t/T")
    fig.suptitle("Modulation y(t) function for each pulse")
    fig.tight_layout()
    fig.savefig("modulation_functions.png", dpi=300)
    print("Modulation saved.")
