# AC-Magnetometry: Pulse Sequence Comparison (Ramsey vs Hahn Echo vs CPMG)

The purpose of this project is to compare how well different dynamical-decoupling pulse sequences detect an oscillating (AC) magnetic field — the core technique behind real quantum magnetometers used for current sensing, vibration monitoring, and structural health monitoring.

## The physics background

A qubit sensor accumulates phase  

$$ \phi = \gamma * \int y(t) B(t) dt$$ 

during a sensing sequence, where y(t) is a "modulation function" that flips sign at every pi-pulse. Ramsey (no pulses) is a DC-sensitive low-pass filter. Hahn echo (one pulse) and CPMG-N (N pulses) act as increasingly narrow bandpass filters centered near *N/(2T)*. This means the right pulse sequence depends on what frequency we're trying to detect — exactly the "lock-in" logic used in real AC magnetometry (e.g. detecting 50/60 Hz grid current, or a specific vibration frequency in a structural-monitoring application).


## Files (in recommended order)

| Day | File | What it does |
|---|---|---|
| 1 | `pulse_sequences.py` | Defines the modulation function y(t) for Ramsey/Hahn/CPMG-N. Run it to sanity-check the pulse timing (`modulation_functions.png`). |
| 2 | `filter.py` | Computes each sequence's frequency-domain filter function via a numerical Fourier integral. Produces `filter_func.png` — the key result showing each sequence's resonance peak. |
| 3 | `noisy_signal.py` | Adds a realistic Lorentzian noise spectrum (finite correlation time) and computes (a) coherence decay under that noise and (b) the deterministic phase response to an AC signal. Produces `coherence_decay.png`. |
| 3-4 | `analysis.py` | Combines signal response + noise-limited coherence into a sensitivity metric, sweeps signal frequency, and reports (via pandas) which sequence is optimal at each frequency. Produces `sensitivity_comparison.png` and `sensitivity_results.csv`. |
| optional | `qutip.ipynb` | Independent check using QuTiP's master-equation solver instead of the filter-function shortcut. |

## Possible further development
 
- **Realistic units**: replace the natural units (`GAMMA = 1.0`) with
  NV-center numbers (`gamma_e / 2pi ≈ 28 GHz/T`) and typical T2*/T2
  values (~1 µs / ~1 ms) to get an actual field sensitivity in T/√Hz —
  directly comparable to published NV magnetometer specs.
- **1/f noise**: swap the Lorentzian PSD for a `1/f` power law (more
  realistic for many solid-state qubits) and see how the optimal
  sequence choice changes — this is an open research question in the
  DD literature.
- **Non-ideal pulses**: replace instantaneous pi-pulses with finite-
  duration pulses (this is where QuTiP's `mesolve` genuinely earns its
  keep over the filter-function shortcut, since finite pulse width
  breaks the simple y(t) picture).
- **Real target signal**: if you want to tie this back to the
  structural/grid-monitoring idea directly, replace the single-tone
  AC signal with something like a power-line harmonic spectrum (50 Hz
  + odd harmonics) and ask which CPMG order best isolates the
  fundamental from the harmonics.
