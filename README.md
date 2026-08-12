# AC-Magnetometry: Pulse Sequence Comparison (Ramsey vs Hahn Echo vs CPMG)

The purpose of this project is to compare how well different dynamical-decoupling pulse sequences detect an oscillating (AC) magnetic field — the core technique behind real quantum magnetometers used for current sensing, vibration monitoring, and structural health monitoring.

## The physics background

A qubit sensor accumulates phase  `$\phi = \gamma * \int y(t) B(t) dt$` during a sensing sequence, where y(t) is a "modulation function" that flips sign at every pi-pulse. Ramsey (no pulses) is a DC-sensitive low-pass filter. Hahn echo (one pulse) and CPMG-N (N pulses) act as increasingly narrow bandpass filters centered near *N/(2T)*. This means the right pulse sequence depends on what frequency we're trying to detect — exactly the "lock-in" logic used in real AC magnetometry (e.g. detecting 50/60 Hz grid current, or a specific vibration frequency in a structural-monitoring application).


## Files (in recommended order)


