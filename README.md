# Uncharacterized In-Situ Setting-Dependent Propagation Delay and Temporal Coincidence Bounds in Photonic Bell Tests

This repository contains the simulation code and vector figures for the manuscript **"Uncharacterized In-Situ Setting-Dependent Propagation Delay and Temporal Coincidence Bounds in Photonic Bell Tests"**.

It evaluates how active basis-switching transients in electro-optic modulators (EOMs) dynamically shift photon arrival times relative to the rigid software coincidence window ($2\Delta t_{\text{window}}$), acting as a physical, setting-dependent data selector that systematically bypasses classical Bell ceilings.

## Theoretical Background

In high-speed loophole-free Bell tests, active switching of EOMs draws sharp capacitive transient currents of up to **$2.0\text{ A}$**. This creates two compounding physical timing delay mechanisms that scale to the picosecond level:

1. **Driver-Induced Discriminator Jitter (Electronic):** The transient current draw induces local electronic ground bounce and rail sag within the shared receiver and TDC chassis. A $\approx 5\text{--}10\text{ mV}$ rail sag shifts comparator thresholds, which translates directly to a **$1.25\text{ to }10\text{ ps}$** time-tag delay.
2. **Dynamic PMD Splitting (Optical):** Underdamped polarization ringing projects the photon wavepacket across both the slow and fast axes of the birefringent routing fiber ($\approx 1.0\text{ to }5.0\text{ ps}$), splitting the wavepacket and shifting the arrival-time center of mass.

This shift pushes borderline photons outside the rigid temporal coincidence window, creating a physics-grounded instantiation of Pearle's data-rejection framework.

## Repository Directory Structure

*   `chronos_simulation.py`: The Python simulation script implementing the setting-dependent temporal filtering models, Parker dispersion linear programs, and quantum DI-QKD secure key rate auditing protocols.
*   `generate_chronos_schematics.py`: The Python script to generate the multi-panel vector schematic illustrating the systematic mechanism.
*   `chronos_schematic.svg`: The multi-panel vector schematic showing EOM ringing, dynamic chirp, and coincidence window filtering.
*   `LICENSE`: MIT License.
*   `README.md`: This description file.

## Running the Simulation

Execute the core numerical integration script to verify the unified spatial-temporal correlation bounds and LP solver:

```bash
python chronos_simulation.py
```

### Calibrated Physical Parameters (Defaults)

*   **Detector Jitter ($\sigma_j$):** $100\text{ ps}$
*   **Coincidence Half-Width ($t_{\text{window}}$):** $150\text{ ps}$
*   **Common-Mode Timing Sag ($\tau_{\text{common}}$):** $15\text{ ps}$
*   **Differential Timing Sag ($\tau_{\text{diff}}$):** $5\text{ ps}$
*   **Quadrature Points:** $1000$

The script evaluates the Common-Mode Timing Lemma, runs a parameter sweep for different timing sags, assesses alternative delay models (cosine-squared, square, linear), and runs a security rate sweep for DI-QKD secure key extraction.

## Generating the Figures

Regenerate the vector diagram:

```bash
python generate_chronos_schematics.py
```

This updates `chronos_schematic.svg` (and generates a local PDF version if required).
