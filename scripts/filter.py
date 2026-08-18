import numpy as np
import matplotlib.pyplot as plt
from pulse_sequences import modulation
from pulse_sequences import SEQUENCES


def filter_fun(omega, T, n_pulses, n_points=20000):
    t = np.linspace(0, T, n_points)
    y = modulation(t, T, n_pulses)
    omega = np.atleast_1d(np.asarray(omega))

    phase = np.exp(1j * np.outer(omega, t))
    intgrand = phase * y[None, :]
    chi = np.trapezoid(intgrand, t, axis=1)
    F = np.abs(chi) ** 2
    return F


def normalized_filter(omega, T, n_pulses, n_points=20000):
    F = filter_fun(omega, T, n_pulses, n_points)
    return F / (T ** 2)  # Ramsey dc peak T^2


if __name__ == "__main__":
    T = 1.0
    omega = np.linspace(0.01, 10*np.pi, 1000)

    fig, ax = plt.subplots(figsize=(12, 8))

    for name, n in SEQUENCES.items():
        F = normalized_filter(omega, T, n)
        f_peak = (omega / (2*np.pi))[np.argmax(F)]
        ax.plot(omega / (2*np.pi), F,
                label=f"{name} (peak at f= {f_peak:.2f}/T)")

    ax.set_xlabel("Signal frequency f = omega / 2*pi [1/T]", fontsize=15)
    ax.set_ylabel("Normalized filter function  F(omega) / T^2", fontsize=15)
    ax.set_title("Frequency sensitivity of each pulse sequence", fontsize=25)
    ax.legend(fontsize=10)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 20)
    fig.tight_layout()
    fig.savefig(
        "/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/results/filter_func.png", dpi=300)
    print("Filter function saved in results directory.")
