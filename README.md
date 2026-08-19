# AC-Magnetometry: Pulse Sequence Comparison (Ramsey vs Hahn Echo vs CPMG)

The purpose of this project is to compare how well different dynamical-decoupling pulse sequences detect an oscillating (AC) magnetic field — the core technique behind real quantum magnetometers used for current sensing, vibration monitoring, and structural health monitoring.
For more information about the background and results please check [the documentation](docs/SCQIS_Project-1.pdf).

## How to start

After pulling the repo to your computer, you can easily create a virtual environment, where all the script will work by 
```
$ conda env create --name YOUR_ENV_NAME --file environment.yml
```
Or you can use your virtual environment with the following requirements:
```
numpy
scipy
pandas
matplotlib
qutip   # optional, only needed for qutip_verification.py
```


## Files (in recommended order)

| File | What it does |
|---|---|
| `pulse_sequences.py` | Defines the modulation function y(t) for Ramsey/Hahn/CPMG-N. Run it to sanity-check the pulse timing (`modulation_functions.png`). |
| `filter.py` | Computes each sequence's frequency-domain filter function via a numerical Fourier integral. Produces `filter_func.png` — the key result showing each sequence's resonance peak. |
| `noisy_signal.py` | Adds a realistic Lorentzian noise spectrum (finite correlation time) and computes (a) coherence decay under that noise and (b) the deterministic phase response to an AC signal. Produces `coherence_decay.png`. |
| `analysis.py` | Combines signal response + noise-limited coherence into a sensitivity metric, sweeps signal frequency, and reports (via pandas) which sequence is optimal at each frequency. Produces `sensitivity_comparison.png` and `sensitivity_results.csv`. |
| `visualization.ipynb` | Independent check using QuTiP's master-equation solver instead of the filter-function shortcut. |
| `enc_dataset.py` | Creating a syntetic dataset to simulate real life lab noisy environment. |
| `final_sensing_experiment.py` | Test ssensing program by applying on the `lab_dataset.csv` file  |

## Possible further development
 
- **Realistic units**: replace the natural units (`GAMMA = 1.0`) with
  NV-center numbers (`gamma_e / 2pi ≈ 28 GHz/T`) and typical T2*/T2
  values (~1 µs / ~1 ms) to get an actual field sensitivity in T/√Hz
- **1/f noise**: swap the Lorentzian PSD for a `1/f` power law (more
  realistic for many solid-state qubits) and see how the optimal
  sequence choice changes — this is an open research question in the
  DD literature.
- **Non-ideal pulses**: replace instantaneous pi-pulses with finite-
  duration pulses (this is where QuTiP's `mesolve`  over the filter-function shortcut, since finite pulse width
  breaks the simple y(t) picture).
- **Real target signal**: replace the single-tone
  AC signal with something like a power-line harmonic spectrum (50 Hz
  + odd harmonics) and ask which CPMG order best isolates the
  fundamental from the harmonics.
