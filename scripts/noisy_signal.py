import numpy as np
import matplotlib.pyplot as plt
from pulse_sequences import modulation, SEQUENCES
from filter import filter_fun

GAMMA = 1.0


def lorentz_psd(omega, noise_amp, tau_c):
    return 2 * noise_amp**2 * tau_c / (1 + (omega*tau_c)**2)


def coherence_decay(T, n_pulses, noise_amp, tau_c, n_omega=800):
    omega_max = min(50 / tau_c + 50*np.pi / T, 2000)
    omega = np.linspace(1e-4, omega_max, n_omega)

    S = lorentz_psd(omega, noise_amp, tau_c)
    F = filter_fun(omega, T, n_pulses, n_points=max(500, 60*max(n_pulses, 1)))
    chi2 = (GAMMA**2 / (2*np.pi) * np.trapezoid(S*F, omega))
    return np.exp(-chi2)


def signal_response(T, n_pulses, AC, omega_signal):
    n_points = 20000
    t = np.linspace(0, T, n_points)
    y = modulation(t, T, n_pulses)
    intgrand = y * np.cos(omega_signal * t)
    overlap = np.trapezoid(intgrand, t)
    phi = GAMMA * AC * overlap
    return phi


if __name__ == "__main__":
    T_values = np.linspace(0.05, 3.0, 25)
    noise_amp, tau_c = 1.0, 0.3

    fig, ax = plt.subplots(figsize=(12, 8))
    for name, n in SEQUENCES.items():
        C = [coherence_decay(T, n, noise_amp, tau_c) for T in T_values]
        ax.plot(T_values, C, label=name)

    ax.set_xlabel("Total sensing time T", fontsize=15)
    ax.set_ylabel(
        "Coherence $|<\sigma_+> (T)>| / |<\sigma_+> (0) |$", fontsize=15)
    ax.set_title(
        rf"Decoherence under Lorentzian noise $\tau_c$ = {tau_c}", fontsize=25)
    ax.grid(True)
    ax.legend(fontsize=15)
    fig.tight_layout()
    fig.savefig(
        "/Users/farkasbende/Desktop/UCPH_Master/SCQIS/project_magnetometry/results/coherence_decay.png", dpi=300)
    print("Coherence decay saved in the results dir.")
